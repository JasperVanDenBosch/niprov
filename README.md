niprov
======
provenance for neuroimaging data

[![PyPI version](https://badge.fury.io/py/niprov.svg)](http://badge.fury.io/py/niprov)
[![Build](https://travis-ci.org/ilogue/niprov.svg?branch=master)](https://travis-ci.org/ilogue/niprov)
[![Docs](https://readthedocs.org/projects/niprov/badge/?version=latest)](http://niprov.readthedocs.org/)
[![Coverage](https://img.shields.io/coveralls/ilogue/niprov.svg)](https://coveralls.io/r/ilogue/niprov)
[![Code Quality](https://scrutinizer-ci.com/g/ilogue/niprov/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/ilogue/niprov/?branch=master)

[![Research software impact](http://depsy.org/api/package/pypi/niprov/badge.svg)](http://depsy.org/package/python/niprov)
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.46136.svg)](http://dx.doi.org/10.5281/zenodo.46136)
[![Twitter](https://img.shields.io/twitter/follow/niprovenance.svg?style=social)](https://twitter.com/niprovenance)


See the [full online documentation](http://niprov.readthedocs.org/) (or [pdf](https://media.readthedocs.org/pdf/niprov/latest/niprov.pdf)) and [PyPi package](https://pypi.python.org/pypi/niprov) and follow [niprov on twitter](https://twitter.com/niprovenance)!

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
----------

```python
import niprov
niprov.discover('.')
analysispackage.correctmotion(input='JD-fmri.nii', output='JD-fmri-3dmc.nii')
niprov.log('JD-fmri.nii', 'motion correction', ['JD-fmri-3dmc.nii'])
niprov.record('mcflirt -in t1flip_all_orig -out t1all_reg -refvol 0')
files = niprov.report(forSubject='John Doe')
```

Web browser
-----------

By running the command `provenance serve` we can start a mini webserver in the
background, and browse images in your webbrowser:

![niprov_search](https://cloud.githubusercontent.com/assets/1508492/16635983/2c4c78fe-438a-11e6-868d-51d26c9956cf.png)
![niprov_details](https://cloud.githubusercontent.com/assets/1508492/16635948/f962ff1c-4389-11e6-958b-59a8fd9de9cd.png)
![niprov_pipeline](https://cloud.githubusercontent.com/assets/1508492/16635949/faa0c8b4-4389-11e6-87ae-87dce26c9973.png)


