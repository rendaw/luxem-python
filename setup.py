from distutils.core import setup, Extension

setup(
    name = 'luxem', 
    version = '0.1', 
    description = 'Luxem is a typed data serialization format similar to JSON.', 
    author = 'Rendaw', 
    author_email = 'rendaw@zarbosoft.com', 
    url = 'http://www.zarbosoft.com/luxem', 
    long_description = 'Luxem is a typed data serialization format similar to JSON.',
    ext_modules = [
        Extension(
            '_luxem', 
            sources = [
                    '_luxem.c',
                    'c/luxem_rawread.c',
                    'c/luxem_rawwrite.c',
                    'c/luxem_internal_common.c',
            ]
        )
    ]
)
