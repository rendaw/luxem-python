import luxem

config = None

def process(batch):
    print 'processing batch {}'.format(batch)

with open('export.luxem', 'r') as import_file:
    reader = luxem.Reader()

    def read_root(root_object):
        def store_config(read_config):
            config = read_config
        root_object.struct('config', store_config)

        def read_input(input_array):
            def process_input(batch):
                optional = False
                if isinstance(batch, luxem.Typed):
                    if batch.name == 'optional':
                        optional = True
                    batch = batch.value
                try:
                    process(batch)
                except:
                    if not optional:
                        raise
            input_array.element(process_input)
        root_object.array('inputs', read_input)
    reader.element(read_root, luxem.object)

    reader.feed(import_file)
