niprov
======
provenance for neuroimaging data

[![Build](https://travis-ci.org/ilogue/niprov.svg?branch=master)](https://travis-ci.org/ilogue/niprov)
[![Docs](https://readthedocs.org/projects/niprov/badge/?version=latest)](http://niprov.readthedocs.org/)
[![Coverage](https://img.shields.io/coveralls/ilogue/niprov.svg)](https://coveralls.io/r/ilogue/niprov)
[![DOI](https://zenodo.org/badge/7344/ilogue/niprov.svg)](http://dx.doi.org/10.5281/zenodo.13683)

See the [full online documentation](http://niprov.readthedocs.org/) (or [pdf](https://media.readthedocs.org/pdf/niprov/latest/niprov.pdf)) and [PyPi package](https://pypi.python.org/pypi/niprov).

To inspect image files, install `nibabel`,`mne` and/or `pydicom`.

A list with all provenance attributes collected can be found [here](http://niprov.readthedocs.org/en/latest/provenance-fields.html).

Commandline Usage
-----------------

*Look for image files below the current directory, inspect them and store the obtained provenance metadata:*
```shell
provenance discover .
```

*Run a transformation command and log it as provenance for the new file:*
```shell
provenance record mcflirt -in t1flip_all_orig -out t1all_reg -refvol 0
```

*Alternatively, log the provenance after running the command:*
```shell
provenance log 'motion correction' --new fmri-3dmc.nii --parent fmri.nii 
```

*Publish provenance of known files for subject 'John Doe' as an html file:*
```shell
provenance report --subject "John Doe" --html
```

Python API
-----------------

```python
import niprov
niprov.discover('.')
analysispackage.correctmotion(input='JD-fmri.nii', output='JD-fmri-3dmc.nii')
niprov.log('JD-fmri.nii', 'motion correction', ['JD-fmri-3dmc.nii'])
niprov.record('mcflirt -in t1flip_all_orig -out t1all_reg -refvol 0')
files = niprov.report(forSubject='John Doe')
```


