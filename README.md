niprov
======
provenance for neuroimaging data

[![Build Status](https://travis-ci.org/ilogue/niprov.svg?branch=master)](https://travis-ci.org/ilogue/niprov)
[![Docs Status](https://readthedocs.org/projects/niprov/badge/?version=latest)](http://niprov.readthedocs.org/)

See the [full documentation](http://niprov.readthedocs.org/).

To inspect image files, install `nibabel` and/or `pydicom`.

Commandline Usage
-----------------

```
discover .
```
*Look for image files below the current directory, inspect them and store the obtained provenance metadata.*

```
provenance --subject "John Doe" --html
```
*Publish provenance of known files for subject 'John Doe' as an html file.*

Python Usage
-----------------

```
import niprov
niprov.discover('.')
files = niprov.report(forSubject='John Doe')
```


