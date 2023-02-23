from setuptools import setup, Extension

module = Extension('search', sources=['search/search.c'])

setup(name='search',
      version='1.0',
      description='Example module that uses C code',
      ext_modules=[module])
