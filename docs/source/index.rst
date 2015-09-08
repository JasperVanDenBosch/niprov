.. niprov documentation master file, created by
   sphinx-quickstart on Thu Jan  1 15:47:37 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

niprov
======

Ever encountered a file of which you weren't sure what analysis steps it had 
gone through? Ever wanted to know what types of data you have available for a 
subject in one overview? Automatically document an analysis pipeline?

Provenance is meta-data that tracks the 'history' of a file, and niprov is a 
python program to create, store and publish provenance for brain imaging files.

To get started, install niprov using pip:
::

    pip install niprov


Keep in mind that to open image files you may need other libraries, such as 
mne-python, nibabel or pydicom.

The next step is to look through your directories for image files:
::

    provenance discover /my/data/dir


After which you can start looking at what you've collected:
::

    provenance report

You can do the same in python code:
::

    import niprov
    niprov.discover('.')
    print(niprov.report()) #this will return a list of dictionaries

Read on to see other features and options.

Get in touch if you have questions or suggestions, by submitting an *issue* on http://github.com/ilogue/niprov or  via email to jasperb@uw.edu.



Contents:

.. toctree::
   :maxdepth: 4

   commandline-usage
   code-examples
   configuration
   provenance-fields
   niprov




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

