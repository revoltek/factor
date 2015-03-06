pipeline.steps=[model]

model.control.kind=recipe
model.control.type=executable_args
model.control.opts.executable=/usr/bin/python
model.control.opts.mapfiles_in=[{{ input_datamap }}, {{ output_datamap }}]
model.control.opts.inputkeys=[inputmodel, outputmodel]
model.control.opts.arguments=[{{ scriptname }}, inputmodel, {{ nterms }}, outputmodel]
model.control.opts.max_per_node={{ ncpu }}
