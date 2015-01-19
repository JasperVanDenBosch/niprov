Commandline Usage
=================

Look for image files below the current directory, inspect them and store the obtained provenance metadata. 
::

    discover .


Run a transformation command and log it as provenance for the new file:
::

    record mcflirt -in t1flip_all_orig -out t1all_reg -refvol 0


Alternatively, log the provenance after running the command:
::

    log 'motion correction' fmri.nii fmri-3dmc.nii


Publish provenance of known files for subject 'John Doe' as an html file.
::

    provenance --subject "John Doe" --html

