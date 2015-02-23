pipeline.steps=[casapy1, mask, casapy2]

casapy1.control.kind=recipe
casapy1.control.type=casapy
casapy1.control.opts.mapfile_in={{ input_datamap_image1 }}
casapy1.control.opts.mapfile_out={{ output_datamap_image1 }}
casapy1.control.opts.inputkey=clean.vis
casapy1.control.opts.outputkey=clean.imagename
casapy1.control.opts.arguments=[--nologger,--log2term,--nogui,-c]
casapy1.parsetarg.clean.gridmode='widefield'
casapy1.parsetarg.clean.wprojplanes={{ wplanes }}
casapy1.parsetarg.clean.selectdata=True
casapy1.parsetarg.clean.uvrange='{{ uvrange }}'
casapy1.parsetarg.clean.mode='mfs'
casapy1.parsetarg.clean.nterms={{ nterms }}
casapy1.parsetarg.clean.niter={{ niter }}
casapy1.parsetarg.clean.gain=0.01
casapy1.parsetarg.clean.threshold='{{ threshold }}'
casapy1.parsetarg.clean.psfmode='clark'
casapy1.parsetarg.clean.interactive=False
casapy1.parsetarg.clean.imsize=[{{ imsize }}, {{ imsize }}]
casapy1.parsetarg.clean.cell=['{{ cell }}', '{{ cell }}']
casapy1.parsetarg.clean.weighting='briggs'
casapy1.parsetarg.clean.robust=-0.25
casapy1.parsetarg.clean.uvtaper=False
casapy1.parsetarg.clean.pbcor=False
casapy1.parsetarg.clean.minpb=0.2
casapy1.parsetarg.clean.multiscale={{ scales }}
casapy1.parsetarg.clean.mask=[]

mask.control.kind=recipe
mask.control.type=executable_args
mask.control.opts.executable=/usr/bin/python
mask.control.opts.mapfile_in={{ input_datamap_mask }}
mask.control.opts.inputkey=inputms
mask.control.opts.arguments=[{{ maskscriptname }}, inputms]

casapy2.control.kind=recipe
casapy2.control.type=casapy
casapy2.control.opts.mapfiles_in=[{{ input_datamap_image1 }}, {{ output_datamap_mask }}]
casapy2.control.opts.mapfile_out={{ output_datamap_image2 }}
casapy2.control.opts.inputkeys=[clean.vis, clean.mask]
casapy2.control.opts.outputkey=clean.imagename
casapy2.control.opts.arguments=[--nologger,--log2term,-c]
casapy2.parsetarg.clean.gridmode='widefield'
casapy2.parsetarg.clean.wprojplanes={{ wplanes }}
casapy2.parsetarg.clean.selectdata=True
casapy2.parsetarg.clean.uvrange='{{ uvrange }}'
casapy2.parsetarg.clean.mode='mfs'
casapy2.parsetarg.clean.nterms={{ nterms }}
casapy2.parsetarg.clean.niter={{ niter }}
casapy2.parsetarg.clean.gain=0.01
casapy2.parsetarg.clean.threshold='{{ threshold }}'
casapy2.parsetarg.clean.psfmode='clark'
casapy2.parsetarg.clean.interactive=False
casapy2.parsetarg.clean.imsize=[{{ imsize }}, {{ imsize }}]
casapy2.parsetarg.clean.cell=['{{ cell }}', '{{ cell }}']
casapy2.parsetarg.clean.weighting='briggs'
casapy2.parsetarg.clean.robust=-0.25
casapy2.parsetarg.clean.uvtaper=False
casapy2.parsetarg.clean.pbcor=False
casapy2.parsetarg.clean.minpb=0.2
casapy2.parsetarg.clean.multiscale={{ scales }}
casapy2.parsetarg.clean.mask=[]
