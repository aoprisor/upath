from setuptools import Extension, setup

extension = Extension("upath", ["upath/upath.c", ], extra_compile_args=["-O3"])

setup(
    name="upath",
    version="1.2",
    author='Georgian-Andrei Oprișor',
    author_email='gaoprisor@gmail.com',
    description="""
    C extension to fetch an item from a nested structure made out of dictionaries and/or lists. 
    Can reduce the time spent retrieving items from nested structures resulted after de-serializing JSON content 
    or other nested structures.
    """,
    ext_modules=[extension]
)
