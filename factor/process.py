"""
Module that preforms the processing
"""
import sys
import os
import numpy as np
import logging
import pickle
from lofarpipe.support.data_map import DataMap
import factor
import factor.directions
import factor.parset
import factor.cluster
from factor.operations.field_ops import *
from factor.operations.facet_ops import *
from factor.lib.scheduler import Scheduler
from factor.lib.direction import Direction


def run(parset_file, logging_level='info', dry_run=False, test_run=False):
    """
    Processes a dataset

    Parameters
    ----------
    parset_file : str
        Filename of parset containing processing parameters
    logging_level : str, optional
        One of 'degug', 'info', 'warning' in decreasing order of verbosity
    dry_run : bool, optional
        If True, do not run pipelines. All parsets, etc. are made as normal
    test_run : bool, optional
        If True, use test settings. These settings are for testing purposes
        only and will not produce useful results

    """
    factor._logging.set_level(logging_level)
    log = logging.getLogger('factor')

    parset = factor.parset.parset_read(parset_file)
    parset['logging_level'] = logging_level

    # Prepare vis data
    bands = []
    from factor.lib.band import Band
    for ms in parset['mss']:
        band = Band(ms, parset['dir_working'], test_run=test_run)
        band.dirindparmdb = os.path.join(band.file, parset['parmdb_name'])
        if not os.path.exists(band.dirindparmdb):
            log.critical('Direction-independent instument parmdb not found '
                'for band {0}'.format(band.file))
            sys.exit(1)
        band.skymodel_dirindep = None
        msbase = os.path.basename(ms)
        if msbase in parset['ms_specific']:
            if 'init_skymodel' in parset['ms_specific'][msbase]:
                band.skymodel_dirindep = parset['ms_specific'][msbase]['init_skymodel']
        bands.append(band)

    # Sort bands by frequency
    band_freqs = [band.freq for band in bands]
    bands = np.array(bands)[np.argsort(band_freqs)].tolist()

    # Get clusterdesc, node info, etc.
    cluster_parset = parset['cluster_specific']
    if 'clusterdesc_file' not in cluster_parset:
        parset['cluster_specific']['clusterdesc'] = 'local.clusterdesc'
    else:
        if cluster_parset['clusterdesc_file'].lower() == 'pbs':
            parset['cluster_specific']['clusterdesc'] = factor.cluster.make_pbs_clusterdesc()
        else:
            parset['cluster_specific']['clusterdesc'] = cluster_parset['clusterdesc_file']
    if not 'node_list' in cluster_parset:
        parset['cluster_specific']['node_list'] = factor.cluster.get_compute_nodes(
            parset['cluster_specific']['clusterdesc'])

    # Get paths to required executables
    factor.cluster.find_executables(parset)

    # Set up scheduler for operations (pipeline runs)
    ndir_simul = len(parset['cluster_specific']['node_list']) * parset['cluster_specific']['ndir_per_node']
    scheduler = Scheduler(parset['genericpipeline_executable'], max_procs=ndir_simul,
        dry_run=dry_run)

    # Make direction object for the field
    field = Direction('field', bands[0].ra, bands[0].dec,
        factor_working_dir=parset['dir_working'])
    exists = field.load_state()
    if not exists:
        field.save_state()

    # Run initial sky model generation and create empty datasets. First check that
    # this operation is needed (only needed if band lacks an initial skymodel or
    # the SUBTRACTED_DATA_ALL column).
    bands_init_subtract = []
    for band in bands:
        if band.skymodel_dirindep is None or not band.has_sub_data:
            bands_init_subtract.append(band)
    if len(bands_init_subtract) > 0:
        op = InitSubtract(parset, bands_init_subtract, field)
        scheduler.run(op)
        field.cleanup()
    else:
        log.info("Sky models found for all MS files. Skipping initsubtract "
            "operation")

    # Define directions. First check for user-supplied file, then for Factor-generated
    # file from a previous run, then for parameters needed to generate it internally
    dir_parset = parset['direction_specific']
    if 'directions_file' in parset:
        directions = factor.directions.directions_read(parset['directions_file'],
            parset['dir_working'])
    elif os.path.exists(os.path.join(parset['dir_working'], 'factor_directions.txt')):
        directions = factor.directions.directions_read(os.path.join(parset['dir_working'],
            'factor_directions.txt'), parset['dir_working'])
    else:
        if 'flux_min_jy' not in dir_parset or \
            'size_max_arcmin' not in dir_parset or \
            'separation_max_arcmin' not in dir_parset:
                log.critical('If no directions file is specified, you must '
                    'give values for flux_min_Jy, size_max_arcmin, and '
                    'separation_max_arcmin')
                sys.exit(1)
        else:
            # Make directions from dir-indep sky models using flux and size parameters
            log.info("No directions file given. Selecting directions internally...")
            parset['directions_file'] = factor.directions.make_directions_file_from_skymodel(bands,
                dir_parset['flux_min_jy'], dir_parset['size_max_arcmin'],
                dir_parset['separation_max_arcmin'], directions_max_num=dir_parset['max_num'],
                interactive=parset['interactive'])
            directions = factor.directions.directions_read(parset['directions_file'],
                parset['dir_working'])

    # Load polygons from previous run if possible
    polys_file = os.path.join(parset['dir_working'], 'regions', 'factor_facets.pkl')
    target_has_own_facet = dir_parset['target_has_own_facet']
    if os.path.exists(polys_file):
        with open(polys_file, 'r') as f:
            polys, widths = pickle.load(f)
            widths = [w[0] for w in widths]

    else:
        if 'target_ra' in dir_parset and 'target_dec' in dir_parset and \
            'target_radius_arcmin' in dir_parset:
            target_ra = dir_parset['target_ra']
            target_dec = dir_parset['target_dec']
            target_radius_arcmin = dir_parset['target_radius_arcmin']
        else:
            target_ra = None
            target_dec = None
            target_radius_arcmin = None

        if not target_has_own_facet:
            polys, widths = factor.directions.thiessen(directions,
                check_edges=dir_parset['check_edges'], target_ra=target_ra,
                target_dec=target_dec, target_radius_arcmin=target_radius_arcmin)
        else:
            target = Direction('target', target_ra, target_dec,
                factor_working_dir=parset['dir_working'])
            directions.append(target)
            polys, widths = factor.directions.thiessen(directions,
                check_edges=dir_parset['check_edges'])
        with open(polys_file, 'wb') as f:
            pickle.dump([polys, widths], f)

    # Set various direction attributes
    for i, direction in enumerate(directions):
        direction.load_state()
        direction.cleanup_mapfiles = []
        direction.vertices = polys[i]
        direction.width = widths[i]

        # Set image sizes
        direction.set_image_sizes(test_run=test_run)

        # Set number of bands and channels
        direction.nbands = len(bands)
        direction.nchannels = np.int(np.ceil(np.float(direction.nbands/np.float(5))))

        # Set field center
        direction.field_ra = field.ra
        direction.field_dec = field.dec

        # Save direction state
        direction.save_state()

    # Make DS9 region files so user can check the facets, etc.
    ds9_facet_reg_file = os.path.join(parset['dir_working'], 'regions', 'facets_ds9.reg')
    factor.directions.make_ds9_region_file(directions, ds9_facet_reg_file)
    ds9_calimage_reg_file = os.path.join(parset['dir_working'], 'regions', 'calimages_ds9.reg')
    factor.directions.make_ds9_calimage_file(directions, ds9_calimage_reg_file)

    # Check with user
    if parset['interactive']:
        print("Facet and DDE calibrator regions saved. Please check that they "
            "are OK before continuing.")
        prompt = "Continue processing (y/n)? "
        answ = raw_input(prompt)
        while answ.lower() not in  ['y', 'n', 'yes', 'no']:
            answ = raw_input(prompt)
        if answ.lower() in ['n', 'no']:
            log.info('Exiting...')
            sys.exit()

    # Select subset of directions to process
    if 'ndir_total' in parset['direction_specific']:
        if parset['direction_specific']['ndir_total'] > 0 and \
            parset['direction_specific']['ndir_total'] <= len(directions):
            directions = directions[:parset['direction_specific']['ndir_total']]

    # Select subset of directions to selfcal
    selfcal_directions = directions
    if 'ndir_selfcal' in parset['direction_specific']:
        if parset['direction_specific']['ndir_selfcal'] > 0 and \
            parset['direction_specific']['ndir_selfcal'] <= len(directions):
            selfcal_directions = directions[:parset['direction_specific']['ndir_selfcal']]

    # Ensure that target is included (but not for selfcal)
    if target_has_own_facet:
        names = [d.name for d in directions]
        if target.name not in names:
            directions.append(target)

    direction_groups = factor.directions.group_directions(selfcal_directions,
        one_at_a_time=parset['direction_specific']['one_at_a_time'],
        n_per_grouping=parset['direction_specific']['groupings'])

    # Iterate over direction groups
    first_pass = True
    for direction_group in direction_groups:
        log.info('Processing {0} direction(s) in parallel in this group'.format(
            len(direction_group)))

        # Divide up the nodes and cores among the directions
        direction_group = factor.cluster.divide_nodes(direction_group,
            parset['cluster_specific']['node_list'],
            parset['cluster_specific']['ndir_per_node'],
            parset['cluster_specific']['ncpu'])

        # Add calibrator(s) to empty datasets. These operations
        # must be done in series
        ops = [FacetAdd(parset, bands, d) for d in direction_group]
        for op in ops:
            scheduler.run(op)

        # Do selfcal on calibrator only
        ops = [FacetSelfcal(parset, d) for d in direction_group]
        scheduler.run(ops)

        # Subtract final model(s) from empty field datasets. These operations
        # must be done in series and only on the directions that passed the
        # selfcal check. Also, after this operation is complete for any
        # direction, set flag to indicate all subsequent directions should use
        # the new subtracted-data column
        if dry_run:
            # For dryrun, skip check
            for d in direction_group:
                d.selfcal_ok = True
                d.save_state()
        direction_group_ok = [d for d in direction_group if d.selfcal_ok]
        if first_pass:
            if len(direction_group_ok) > 0:
                # Only use new data if at least one direction is OK
                for i, d in enumerate(directions):
                    # Set flag for *all* directions except first one
                    if i > 0:
                        d.use_new_sub_data = True
                first_pass = False
        else:
            for d in direction_group_ok:
                d.use_new_sub_data = True
        ops = [FacetSub(parset, d) for d in direction_group if d.selfcal_ok]
        for op in ops:
            scheduler.run(op)

        # Lastly, stop Factor if selfcal for any direction in this group failed
        for d in direction_group:
            all_good = True
            if not d.selfcal_ok:
                log.error('Selfcal failed for direction {0}. Please check '
                    'the settings for this direction.'.format(d.name))
                if parset['interactive']:
                    prompt = "Continue with this direction anyway (y/n)? "
                    answ = raw_input(prompt)
                    while answ.lower() not in  ['y', 'n', 'yes', 'no']:
                        answ = raw_input(prompt)
                    if answ.lower() in ['n', 'no']:
                        d.reset_state()
                        all_good = False
                    else:
                        d.selfcal_ok = True
                        d.save_state()
                else:
                    d.reset_state()
                    all_good = False
            else:
                d.save_state()
        if not all_good:
            self.log.info('Exiting...')
            sys.exit(1)

        # Clean up files
        for d in direction_group:
            d.cleanup()

    # Make final facet images (from final empty datasets) if desired. Also image
    # any facets for which selfcal failed or no selfcal was done
    dirs_to_image = [d for d in directions if d.make_final_image and d.selfcal_ok]

    # Add directions without selfcal if desired
    if transfer_selfcal_to_rest:
        dirs_to_transfer = [d for d in directions if not d.selfcal_ok]
        dirs_with_selfcal = [d for d in directions if d.selfcal_ok]

        for d in dirs_to_transfer:
            # Search for nearest direction with successful selfcal
            nearest = factor.directions.find_nearest(d, dirs_with_selfcal)
            d.dir_dep_parmdb_datamap = nearest.dir_dep_parmdb_datamap
        dirs_to_image.append(dirs_to_transfer)

    if len(dirs_to_image) > 0:
        ops = [FacetAddFinal(parset, bands, d) for d in dirs_to_image]
        for op in ops:
            scheduler.run(op)

        # Divide up the nodes and cores among the directions
        dirs_to_image = factor.cluster.divide_nodes(dirs_to_image,
            parset['cluster_specific']['node_list'],
            parset['cluster_specific']['ndir_per_node'],
            parset['cluster_specific']['ncpu'])

        ops = [FacetImageFinal(parset, d) for d in dirs_to_image]
        scheduler.run(ops)

    # Mosaic the final facet images together
    if parset['make_mosaic']:
        field.facet_image_filenames = []
        field.facet_vertices_filenames = []
        for d in directions:
            facet_image = DataMap.load(d.facet_image_mapfile)[0].file
            field.facet_image_filenames.append(facet_image)
            field.facet_vertices_filenames.append(d.save_file)
        op = MakeMosaic(parset, field)
        scheduler.run(op)

    log.info("Factor has finished :)")
