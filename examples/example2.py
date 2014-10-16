import luxem
with open('export.luxem', 'w') as export_file:
    export = luxem.Writer(write_file=export_file, pretty=True).object_begin()
    export.key('config').value({
        'path': '/usr/bin',
        'iterations': 10
    })
    export.key('inputs').array_begin()
    for batch in ['batch001', 'batch002', luxem.Typed('optional', 'batch003')]:
        export.value(batch)
    export.array_end()
    export.object_end()
