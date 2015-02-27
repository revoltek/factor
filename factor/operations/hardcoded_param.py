"""
Module that holds all hard-coded parameters
"""

init_subtract = {
'imagerh' : {'niter': 40000,
             'imsize': 6250,
             'mscale': False,
             'cell': '7.5arcsec',
             'uvrange': "0.08~7.0klambda",
             'threshpix': 4,
             'threshisl': 2.5,
             'atrous_do': True,
             'rmsbox': '(70, 20)',
             'threshold': '0mJy',
             'nterms' : 1},
'modelh' : {'nterms': 1},
'calibh' : {'incol': 'DATA',
            'outcol1': 'SUBTRACTED_DATA',
            'outcol2': 'MODEL_DATA',
            'flags': '--replace-sourcedb'},
'avgl' : {'columnname': 'MODEL_DATA', # outcol is DATA
          'freqstep': 5,
          'timestep': 2},
'imagerl' : {'niter' : 10000,
             'imsize': 4800,
             'mscale': False,
             'cell': '25arcsec',
             'uvrange': "0.08~2.0klambda",
             'threshisl': 5,
             'threshpix': 5,
             'atrous_do': True,
             'rmsbox': '(70, 20)',
             'threshold': '0mJy',
             'nterms': 1},
'modell' : {'nterms': 1},
'calibl' : {'incol': 'SUBTRACTED_DATA',
            'outcol': 'SUBTRACTED_DATA_ALL',
            'flags': '--replace-sourcedb'},
'merge' : {'matchby': 'name',
           'keep': 'all',
           'radius': 0}
}

init_subtract_test = {
'imagerh' : {'niter': 2000,
             'imsize': 6250,
             'mscale': False,
             'cell': '7.5arcsec',
             'uvrange': "0.08~7.0klambda",
             'threshpix': 4,
             'threshisl': 2.5,
             'atrous_do': True,
             'rmsbox': '(70, 20)',
             'threshold': '0mJy',
             'nterms' : 1},
'modelh' : {'nterms': 1},
'calibh' : {'incol': 'DATA',
            'outcol1': 'SUBTRACTED_DATA',
            'outcol2': 'MODEL_DATA',
            'flags': '--replace-sourcedb'},
'avgl' : {'columnname': 'MODEL_DATA', # outcol is DATA
          'freqstep': 5,
          'timestep': 2},
'imagerl' : {'niter' : 2000,
             'imsize': 4800,
             'mscale': False,
             'cell': '25arcsec',
             'uvrange': "0.08~2.0klambda",
             'threshisl': 5,
             'threshpix': 5,
             'atrous_do': True,
             'rmsbox': '(70, 20)',
             'threshold': '0mJy',
             'nterms': 1},
'modell' : {'nterms': 1},
'calibl' : {'incol': 'SUBTRACTED_DATA',
            'outcol': 'SUBTRACTED_DATA_ALL',
            'flags': '--replace-sourcedb'},
'merge' : {'matchby': 'name',
           'keep': 'all',
           'radius': 0}
}

init_subtract_test_quick = {
'imagerh' : {'niter': 200,
             'imsize': 650,
             'mscale': False,
             'cell': '7.5arcsec',
             'uvrange': "0.08~7.0klambda",
             'threshpix': 4,
             'threshisl': 2.5,
             'atrous_do': True,
             'rmsbox': '(70, 20)',
             'threshold': '0mJy',
             'nterms' : 1},
'modelh' : {'nterms': 1},
'calibh' : {'incol': 'DATA',
            'outcol1': 'SUBTRACTED_DATA',
            'outcol2': 'MODEL_DATA',
            'flags': '--replace-sourcedb'},
'avgl' : {'columnname': 'MODEL_DATA', # outcol is DATA
          'freqstep': 5,
          'timestep': 2},
'imagerl' : {'niter' : 200,
             'imsize': 480,
             'mscale': False,
             'cell': '25arcsec',
             'uvrange': "0.08~2.0klambda",
             'threshisl': 5,
             'threshpix': 5,
             'atrous_do': True,
             'rmsbox': '(70, 20)',
             'threshold': '0mJy',
             'nterms': 1},
'modell' : {'nterms': 1},
'calibl' : {'incol': 'SUBTRACTED_DATA',
            'outcol': 'SUBTRACTED_DATA_ALL',
            'flags': '--replace-sourcedb'},
'merge' : {'matchby': 'name',
           'keep': 'all',
           'radius': 0}
}

facet_add_cal = {
'model' : {},
'add' : {'incol': 'SUBTRACTED_DATA_ALL',
         'outcol': 'FACET_DATA',
         'flags': '--replace-sourcedb'},
'shift' : {'columnname': 'FACET_DATA'} # outcol is DATA
}

facet_setup = {
'avg' : {'columnname': 'DATA', # outcol is DATA
          'freqstep': 20,
          'timestep': 1},
'apply' : {'incol': 'DATA',
           'outcol': 'CORRECTED_DATA'},
'concat1' : {'columnname': 'DATA'}, # outcol is DATA
'concat2' : {'columnname': 'CORRECTED_DATA'}, # outcol is DATA
'copy' : {'incol': 'DATA',
          'outcol': 'CORRECTED_DATA'}
}

facet_selfcal = {
'avg0' : {'columnname': 'CORRECTED_DATA', # outcol is DATA
          'freqstep': 1,
          'timestep': 12},
'concat0' : {'columnname': 'DATA'}, # outcol is DATA
'imager0' : {'niter': 1000,
             'imsize': 1024,
             'mscale': True,
             'cell': '1.5arcsec',
             'uvrange': '>80lambda',
             'threshpix': 10.0,
             'threshisl': 6.0,
             'atrous_do': True,
             'rmsbox': '(50, 20)',
             'threshold': '0mJy',
             'nterms' : 2},
'model0' : {'nterms': 2},
'solve_phaseonly1' : {'incol': 'DATA',
                      'outcol': 'CORRECTED_DATA',
                      'chunksize': 200,
                      'uvrange': 80,
                      'flags': '-f'},
'avg1' : {'columnname': 'CORRECTED_DATA', # outcol is DATA
          'freqstep': 1,
          'timestep': 12},
'imager1' : {'niter': 1000,
             'imsize': 1024,
             'mscale': True,
             'cell': '1.5arcsec',
             'uvrange': '>80lambda',
             'threshpix': 10.0,
             'threshisl': 10.0,
             'atrous_do': True,
             'rmsbox': '(60, 20)',
             'threshold': '0mJy',
             'nterms' : 2},
'model1' : {'nterms': 2},
'solve_phaseonly2' : {'incol': 'DATA',
                      'outcol': 'CORRECTED_DATA',
                      'chunksize': 200,
                      'uvrange': 80,
                      'flags': '-f'},
'avg2' : {'columnname': 'CORRECTED_DATA', # outcol is DATA
          'freqstep': 1,
          'timestep': 12},
'imager2' : {'niter': 1000,
             'imsize': 1024,
             'mscale': True,
             'cell': '1.5arcsec',
             'uvrange': '>80lambda',
             'threshpix': 10.0,
             'threshisl': 10.0,
             'atrous_do': True,
             'rmsbox': '(60, 20)',
             'threshold': '0mJy',
             'nterms' : 2},
'model2' : {'nterms': 2},
'solve_phaseamp1_phaseonly': {'incol': 'DATA',
                              'outcol': 'CORRECTED_DATA_PHASE',
                              'uvrange': 80,
                              'flags': '-f'},
'solve_phaseamp1_amponly': {'incol': 'CORRECTED_DATA_PHASE',
                            'uvrange': 80,
                            'flags': '-f'},
'smooth_amp1': {'solset': 'sol000',
                'soltab_amp': 'amplitude000',
                'soltab_phase': 'phase000',
                'smoothing_window': 10},
'apply_amp1' : {'incol': 'CORRECTED_DATA_PHASE',
                'outcol': 'CORRECTED_DATA'},
'avg3' : {'columnname': 'CORRECTED_DATA', # outcol is DATA
          'freqstep': 1,
          'timestep': 12},
'imager3' : {'niter': 1000,
             'imsize': 1024,
             'mscale': True,
             'cell': '1.5arcsec',
             'uvrange': '>80lambda',
             'threshpix': 10.0,
             'threshisl': 10.0,
             'atrous_do': True,
             'rmsbox': '(60, 20)',
             'threshold': '0mJy',
             'nterms' : 2},
'model3' : {'nterms': 2},
'reset_phases' : {'solset': 'sol000',
                  'soltab': 'phase000'},
'apply_amp2' : {'incol': 'DATA',
                'outcol': 'CORRECTED_DATA_AMP'},
'solve_phaseamp2_phaseonly': {'incol': 'CORRECTED_DATA_AMP',
                              'outcol': 'CORRECTED_DATA_PHASE',
                              'uvrange': 80,
                              'flags': '-f'},
'solve_phaseamp2_amponly': {'incol': 'CORRECTED_DATA_PHASE',
                            'uvrange': 80,
                            'flags': '-f'},
'smooth_amp2': {'solset': 'sol000',
                'soltab_amp': 'amplitude000',
                'soltab_phase': 'phase000',
                'smoothing_window': 10},
'apply_amp3' : {'incol': 'CORRECTED_DATA_PHASE',
                'outcol': 'CORRECTED_DATA'},
'avg4' : {'columnname': 'CORRECTED_DATA', # outcol is DATA
          'freqstep': 1,
          'timestep': 12},
'imager4' : {'niter': 1000,
             'imsize': 1024,
             'mscale': True,
             'cell': '1.5arcsec',
             'uvrange': '>80lambda',
             'threshpix': 10.0,
             'threshisl': 10.0,
             'atrous_do': True,
             'rmsbox': '(60, 20)',
             'threshold': '0mJy',
             'nterms' : 2},
'smooth_amp3': {'solset': 'sol000',
                'soltab_amp': 'amplitude000',
                'soltab_phase': 'phase000',
                'smoothing_window': 1},
}

facet_image= {
'add_dirindep' : {'incol': 'SUBTRACTED_DATA_ALL',
                  'outcol': 'FACET_DATA',
                  'flags': '--replace-sourcedb'},
'apply_dirdep' : {'incol': 'FACET_DATA',
                  'outcol': 'CORRECTED_DATA'},
'shift' : {'columnname': 'CORRECTED_DATA'}, # outcol is DATA
'avg' : {'columnname': 'DATA', # outcol is DATA
         'freqstep': 5,
         'timestep': 3},
'imager_template' : {'niter': 1,
                     'imsize': 1024,
                     'mscale': True,
                     'cell': '1.5arcsec',
                     'uvrange': '>80lambda',
                     'threshpix': 10.0,
                     'threshisl': 6.0,
                     'atrous_do': True,
                     'rmsbox': '(70, 20)',
                     'threshold': '0mJy',
                     'nterms' : 2},
'expand_mask' : {'image': ''},
'imager' : {'niter': 10000,
            'imsize': 1024,
            'mscale': True,
            'cell': '1.5arcsec',
            'uvrange': '>80lambda',
            'threshpix': 6.0,
            'threshisl': 3.0,
            'atrous_do': True,
            'rmsbox': '(70, 20)',
            'threshold': '0mJy',
            'nterms' : 2},
'model' : {'nterms': 2}
}

facet_finalize = {
'subtract' : {'incol': 'FACET_DATA',
              'outcol': 'SUBTRACTED_DATA_ALL',
              'flags': '--replace-sourcedb'}
}

facet_final_image= {
'add_dirdep' : {'incol': 'SUBTRACTED_DATA_ALL',
                'outcol': 'FACET_DATA',
                'flags': '--replace-sourcedb'},
'apply_dirdep' : {'incol': 'FACET_DATA',
                  'outcol': 'CORRECTED_DATA'},
'shift' : {'columnname': 'CORRECTED_DATA'}, # outcol is DATA
'avg' : {'columnname': 'DATA', # outcol is DATA
         'freqstep': 5,
         'timestep': 3},
'imager' : {'niter': 10000,
            'imsize': 1024,
            'mscale': True,
            'cell': '1.5arcsec',
            'uvrange': '>80lambda',
            'threshpix': 6.0,
            'threshisl': 3.0,
            'atrous_do': True,
            'rmsbox': '(70, 20)',
            'threshold': '0mJy',
            'nterms' : 2},
'model' : {'nterms': 2}
}
