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

Ever encountered a file of which you weren’t sure what analysis steps it had gone through? 
Ever wanted to know what types of data you have available for a subject in one overview? 
Automatically document an analysis pipeline?

Provenance is meta-data that tracks the ‘history’ of a file, and niprov is a python program to create, store and publish provenance for brain imaging files.

A list with all provenance attributes collected can be found [here](http://niprov.readthedocs.org/en/latest/provenance-fields.html).
Read more in the [full online documentation](http://niprov.readthedocs.org/) (or [pdf](https://media.readthedocs.org/pdf/niprov/latest/niprov.pdf)).
For additional detailed information on image files, install `nibabel`,`mne` and/or `pydicom`.



Commandline Usage
-----------------

Install niprov:
```shell
pip install niprov
```

Look for existing image files in your data directory:
```shell
provenance discover /my/data/directory
```

Run a transformation command and log it as provenance for the new file:
```shell
provenance record mcflirt -in t1flip_all_orig -out t1all_reg -refvol 0
```

Store provenance of known MEG files as an xml file:
```shell
provenance export --modality "MEG" --xml
```

Python API
----------

```python
import niprov
provenance = niprov.ProvenanceContext()

# Log an analysis step:
someAnalysisPackage.correctmotion(input='JD-fmri.nii', output='JD-fmri-3dmc.nii')
provenance.log('JD-fmri.nii', 'motion correction', ['JD-fmri-3dmc.nii'])

# Loop over images of John Smith and display a preview:
for image in provenance.get().bySubject('John Smith'):
    image.viewSnapshot() 

# Make sure two files were acquired with the same parameters:
img1.compare(img2).assertEqualProtocol()
```

Web browser
-----------

By running the command `provenance serve` you can start a mini webserver in the
background, and browse images in your webbrowser:

![niprov_search](https://cloud.githubusercontent.com/assets/1508492/16635983/2c4c78fe-438a-11e6-868d-51d26c9956cf.png)
![niprov_details](https://cloud.githubusercontent.com/assets/1508492/16635948/f962ff1c-4389-11e6-958b-59a8fd9de9cd.png)
![niprov_pipeline](https://cloud.githubusercontent.com/assets/1508492/16635949/faa0c8b4-4389-11e6-87ae-87dce26c9973.png)


