Provenance Fields
=================

Overview of provenance attributes collected:


+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| Field                                       | superficial | transformed | PAR-REC | DICOM | FIF | CNT |
+=============================================+=============+=============+=========+=======+=====+=====+
| :ref:`field-path`                           | yes         | yes         | yes     | yes   | yes | yes |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-hostname`                       | yes         | yes         | yes     | yes   | yes | yes |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-user`                           | yes         | yes         | yes     | yes   | yes | yes |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-location`                       | yes         | yes         | yes     | yes   | yes | yes |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-added`                          | yes         | yes         | yes     | yes   | yes | yes |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-version-added`                  | yes         | yes         | yes     | yes   | yes | yes |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-size`                           | yes         | yes         | yes     | yes   | yes | yes |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-hash`                           | yes         | yes         | yes     | yes   | yes | yes |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-created`                        | yes         | yes         | yes     | yes   | yes | yes |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-transient`                      | yes         | yes         | yes     | yes   | yes | yes |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-modality`                       | yes         | inherited   | yes     | yes   | yes | yes |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-acquired`                       |             | inherited   | yes     | yes   | yes | yes |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-duration`                       |             | inherited   | yes     | yes   | yes | yes |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-subject`                        |             | inherited   | yes     | yes   | yes | yes |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-dimensions`                     |             |             | yes     | maybe | yes | yes |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-project`                        |             | inherited   |         |       | yes |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-protocol`                       |             | inherited   | yes     | yes   |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-subject-position`               |             | inherited   | yes     | yes   |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-water-fat-shift`                |             | inherited   | yes     | yes   |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-transformation`                 |             | yes         |         |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-parent`                         |             | yes         |         |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-code`                           |             | yes         |         |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-logtext`                        |             | yes         |         |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-script`                         |             | yes         |         |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-args`                           |             | yes         |         |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-kwargs`                         |             | yes         |         |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-sampling-frequency`             |             | inherited   |         |       | yes | yes |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-fif-type`                       |             |             |         |       | yes |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-lowpass`                        |             |             |         |       | yes |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-highpass`                       |             |             |         |       | yes |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-bad-channels`                   |             |             |         |       | yes |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-seriesuid`                      |             |             |         | yes   |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-filesInSeries`                  |             |             |         | yes   |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-technique`                      |             | inherited   | yes     |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-repetition-time`                |             | inherited   | yes     |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-field-of-view`                  |             |             | yes     |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-epi-factor`                     |             | inherited   | yes     |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-magnetization-transfer-contrast`|             | inherited   | yes     |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-diffusion`                      |             | inherited   | yes     |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-slice-thickness`                |             |             | yes     |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-slice-orientation`              |             |             | yes     |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-echo-time`                      |             | inherited   | yes     |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-flip-angle`                     |             | inherited   | yes     |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-inversion-time`                 |             | inherited   | yes     |       |     |     |
+---------------------------------------------+-------------+-------------+---------+-------+-----+-----+



.. _field-path:

path
----

The last known path to the file.

.. _field-hostname:

hostname
--------

Hostname of the computer on which the file resides.

.. _field-user:

user
----

Name of the user that created the file and/or registered its provenance.

.. _field-location:

location
--------

A string that combines computer and filesystem path.

.. _field-added:

added
-----

Date and time that the provenance for this file was registered.

.. _field-version-added:

version-added
-------------

A floating point number reflecting the niprov version used to create the
provenance record.


.. _field-size:

size
----

File size.

.. _field-hash:

hash
----

An MD5 hash of the file's binary contents.

.. _field-created:

created
-------

Last known modified date of the file as reported by the OS.

.. _field-transient:

transient
---------

Whether the file is deemed temporary.

.. _field-modality:

modality
--------

Type of data; MRI, DWI, MEG, EEG or other.

.. _field-acquired:

acquired
--------

When the data was collected.

.. _field-duration:

duration
--------

Duration of the acquisition in seconds.

.. _field-subject:

subject
-------

The participant whose brain was imaged.

.. _field-dimensions:

dimensions
----------

Dimensions of the image. Order of dimensions dependent on format; in principle follows (where applicable); in-slice, number of slices, time. E.g. x,z,y,t.

.. _field-project:

project
-------

The name of the research project.

.. _field-protocol:

protocol
--------

The name of the pulse sequence used.

.. _field-subject-position:

subject-position
----------------

The position and orientation of the subject during during the scan. E.g. head first supine.

.. _field-water-fat-shift:

water-fat-shift
---------------

Water fat shift value.

.. _field-transformation:

transformation
--------------

The name of the transformation applied to generate this derivative image.

.. _field-parent:

parent
--------

The file that this file is a transformed version of.

.. _field-code:

code
----

The command used to generate this image.

.. _field-logtext:

logtext
-------

The commandline output of the transformation.

.. _field-script:

script
------

The path to the code file containing the transformation routine.

.. _field-args:

args
----

The positional arguments passed to a python-based transformation command.

.. _field-kwargs:

kwargs
------

The keyword arguments passed to a python-based transformation command.

.. _field-sampling-frequency:

sampling-frequency
------------------

How many samples were acquired per second.

.. _field-fif-type:

fif-type
--------

Type of MNE fiff file. One of 'raw', 'ave', 'epo', 'cov', 'fwd' or 'trans'.

.. _field-lowpass:

lowpass
-------

Cutoff frequency of the lowpass filter applied, in Hz.

.. _field-highpass:

highpass
--------

Cutoff frequency of the highpass filter applied, in Hz.

.. _field-bad-channels:

bad-channels
------------

Names of channels/sensors marked as bad.

.. _field-seriesuid:

seriesuid
---------

A unique identifier for files in a series. Corresponds to `SeriesInstanceUID` in the DICOM format.

.. _field-filesInSeries:

filesInSeries
-------------

A list of paths to files that are part of this series.

.. _field-technique:

technique
---------

The imaging technique that the protocol uses.


.. _field-repetition-time:

repetition-time
---------------

Time to scan one volume


.. _field-field-of-view:

field-of-view
-------------

The extent of the observable world that is seen by the image. This is a list
of three values.


.. _field-epi-factor:

epi-factor
----------

Echo-planar-imaging factor.


.. _field-magnetization-transfer-contrast:

magnetization-transfer-contrast
-------------------------------

A technique that uses the transfer of nuclear spin polarization and/or spin 
coherence from one population of nuclei to another population of nuclei.


.. _field-diffusion:

diffusion
---------

Whether this is a diffusion image. Boolean.


.. _field-slice-thickness:

slice-thickness
---------------

Thickness in mm of the slices. In case the file contains multiple images,
this applies to the first image.


.. _field-slice-orientation:

slice-orientation
-----------------

Spatial orientation of the slices. In case the file contains multiple images,
this applies to the first image.


.. _field-echo-time:

echo-time
---------

The time in milliseconds between the application of the 90° pulse and the peak of the echo signal in Spin Echo and Inversion Recovery pulse sequences.


.. _field-flip-angle:

flip-angle
----------

The angle to which the net magnetization is rotated or tipped relative to the main magnetic field direction via the application of an RF excitation pulse.


.. _field-inversion-time:

inversion-time
---------------

The time period between the 180° inversion pulse and the 90° excitation pulse in an Inversion Recovery pulse sequence. 



