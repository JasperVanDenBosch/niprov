Provenance Fields
=================

Overview of provenance attributes collected:


+-----------------------------+-------------+-------------+---------+-------+
| Field                       | Superficial | transformed | PAR-REC | DICOM |
+=============================+=============+=============+=========+=======+
| :ref:`field-path`           | yes         | yes         | yes     | yes   |
+-----------------------------+-------------+-------------+---------+-------+
| :ref:`field-size`           | yes         | yes         | yes     | yes   |
+-----------------------------+-------------+-------------+---------+-------+
| :ref:`field-hash`           | yes         | yes         | yes     | yes   |
+-----------------------------+-------------+-------------+---------+-------+
| :ref:`field-created`        | yes         | yes         | yes     | yes   |
+-----------------------------+-------------+-------------+---------+-------+
| :ref:`field-acquired`       |             | inherited   | yes     | yes   |
+-----------------------------+-------------+-------------+---------+-------+
| :ref:`field-subject`        |             | inherited   | yes     | yes   |
+-----------------------------+-------------+-------------+---------+-------+
| :ref:`field-protocol`       |             | inherited   | yes     | yes   |
+-----------------------------+-------------+-------------+---------+-------+
| :ref:`field-transformation` |             | yes         |         |       |
+-----------------------------+-------------+-------------+---------+-------+
| :ref:`field-parent`       |             | yes         |         |       |
+-----------------------------+-------------+-------------+---------+-------+
| :ref:`field-code`           |             | yes         |         |       |
+-----------------------------+-------------+-------------+---------+-------+
| :ref:`field-logtext`        |             | yes         |         |       |
+-----------------------------+-------------+-------------+---------+-------+


.. _field-path:

path
----

The last known path to the file.

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

.. _field-acquired:

acquired
--------

When the data was collected.

.. _field-subject:

subject
-------

The participant whose brain was imaged.

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



