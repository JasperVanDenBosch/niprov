Provenance Fields
=================

Overview of provenance attributes collected:


+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| Field                       | superficial | transformed | PAR-REC | DICOM | FIF | CNT |
+=============================+=============+=============+=========+=======+=====+=====+
| :ref:`field-path`           | yes         | yes         | yes     | yes   | yes | yes |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-hostname`       | yes         | yes         | yes     | yes   | yes | yes |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-location`       | yes         | yes         | yes     | yes   | yes | yes |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-size`           | yes         | yes         | yes     | yes   | yes | yes |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-hash`           | yes         | yes         | yes     | yes   | yes | yes |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-created`        | yes         | yes         | yes     | yes   | yes | yes |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-transient`      | yes         | yes         | yes     | yes   | yes | yes |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-acquired`       |             | inherited   | yes     | yes   | yes | yes |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-subject`        |             | inherited   | yes     | yes   | yes | yes |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-dimensions`     |             |             | yes     | maybe | yes | yes |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-project`        |             | inherited   |         |       | yes |     |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-protocol`       |             | inherited   | yes     | yes   |     |     |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-transformation` |             | yes         |         |       |     |     |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-parent`         |             | yes         |         |       |     |     |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-code`           |             | yes         |         |       |     |     |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-logtext`        |             | yes         |         |       |     |     |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-script`         |             | yes         |         |       |     |     |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-args`           |             | yes         |         |       |     |     |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-kwargs`         |             | yes         |         |       |     |     |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-seriesuid`      |             |             |         | yes   |     |     |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+
| :ref:`field-filesInSeries`  |             |             |         | yes   |     |     |
+-----------------------------+-------------+-------------+---------+-------+-----+-----+


.. _field-path:

path
----

The last known path to the file.

.. _field-hostname:

hostname
--------

Hostname of the computer on which the file resides.

.. _field-location:

location
--------

A string that combines computer and filesystem path.

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

.. _field-acquired:

acquired
--------

When the data was collected.

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

.. _field-seriesuid:

seriesuid
---------

A unique identifier for files in a series. Corresponds to `SeriesInstanceUID` in the DICOM format.

.. _field-filesInSeries:

filesInSeries
-------------

A list of paths to files that are part of this series.

