#!/usr/bin/python
# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages


setup(name='niprov',
      version='0.1',
      author='Jasper J.F. van den Bosch',
      author_email='japsai@gmail.com',
      description='provenance for neuroimaging data',
      packages=find_packages(),
      url = 'https://github.com/ilogue/niprov',
      test_suite="tests",
      scripts=['executables/provenance'],
      zip_safe=False,
      classifiers=[
            'License :: OSI Approved :: BSD License',
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering']
      )
