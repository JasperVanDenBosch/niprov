#!/usr/bin/python
# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages
import os

reqs = [
'mock',
'coveralls',
'sphinx',
'mako',
'pymongo',
'shortuuid',
'pyramid',
'pyramid_mako',
'waitress',
]

try:
   import pypandoc
   README = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
   README = ''

setup(name='niprov',
      version='0.3',
      author='Jasper J.F. van den Bosch',
      author_email='japsai@gmail.com',
      description='provenance for neuroimaging data',
      packages=find_packages(),
      url = 'https://github.com/ilogue/niprov',
      test_suite="tests",
      scripts=['executables/provenance'],
      zip_safe=False,
      license='BSD',
      long_description=README,
      classifiers=[
            'License :: OSI Approved :: BSD License',
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering'],
      install_requires=reqs,
      include_package_data=True,
      entry_points="""\
      [paste.app_factory]
      main = niprov:main
      """,
      )
