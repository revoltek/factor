[DEFAULT]
lofarroot = {{ lofarroot }}
pythonpath = {{ lofarpythonpath }}
runtime_directory = {{ runtime_dir }}
recipe_directories = [%(pythonpath)s/lofarpipe/recipes, {{ piperoot }}]
working_directory = {{ working_dir }}
task_files = [%(lofarroot)s/share/pipeline/tasks.cfg, {{ piperoot }}/tasks.cfg]

[layout]
job_directory = %(runtime_directory)s/%(job_name)s

[cluster]
clusterdesc = {{ clusterdesc }}

[deploy]
engine_ppath = %(pythonpath)s:%(pyraproot)s/lib:/opt/cep/pythonlibs/lib/python/site-packages
engine_lpath = %(lofarroot)s/lib:%(casaroot)s/lib:%(pyraproot)s/lib:%(hdf5root)s/lib:%(wcsroot)s/lib

[logging]
log_file = %(runtime_directory)s/%(job_name)s/logs/%(start_time)s/pipeline.log
xml_stat_file = %(runtime_directory)s/%(job_name)s/logs/%(start_time)s/statistics.xml

{{ remote }}
