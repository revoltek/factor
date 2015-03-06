pipeline.steps=[casapy1]

casapy1.control.kind=recipe
casapy1.control.type=casapy
casapy1.control.opts.mapfile_in={{ vis_datamap_image1 }}
casapy1.control.opts.inputkey=clean.vis
casapy1.control.opts.outputkey=clean.imagename
casapy1.control.opts.arguments=[--nologger,--log2term,--nogui,-c]
casapy1.control.opts.max_per_node=1
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
