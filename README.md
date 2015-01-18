niprov
======
provenance for neuroimaging data

[![Build](https://travis-ci.org/ilogue/niprov.svg?branch=master)](https://travis-ci.org/ilogue/niprov)
[![Docs](https://readthedocs.org/projects/niprov/badge/?version=latest)](http://niprov.readthedocs.org/)
[![Coverage](https://img.shields.io/coveralls/ilogue/niprov.svg)](https://coveralls.io/r/ilogue/niprov)
[![DOI](https://zenodo.org/badge/7344/ilogue/niprov.svg)](http://dx.doi.org/10.5281/zenodo.13683)

See the [full documentation](http://niprov.readthedocs.org/) and [PyPi package](https://pypi.python.org/pypi/niprov).

To inspect image files, install `nibabel` and/or `pydicom`.

Commandline Usage
-----------------

```
discover .
```
*Look for image files below the current directory, inspect them and store the obtained provenance metadata.*

```
    record 'motion correction' fmri.nii fmri-3dmc.nii
```
*Add provenance for a new file created as a result of an existing file*

```
provenance --subject "John Doe" --html
```
*Publish provenance of known files for subject 'John Doe' as an html file.*

Python API
-----------------

```
import niprov
niprov.discover('.')
analysispackage.correctmotion(input='JD-fmri.nii', output='JD-fmri-3dmc.nii')
niprov.record('motion correction', 'JD-fmri.nii','JD-fmri-3dmc.nii')
files = niprov.report(forSubject='John Doe')
```


