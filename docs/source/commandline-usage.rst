Commandline Usage
=================

Look for image files below the current directory, inspect them and store the obtained provenance metadata. 
::

    provenance discover .


Run a transformation command and log it as provenance for the new file:
::

    provenance record mcflirt -in t1flip_all_orig -out t1all_reg -refvol 0


Alternatively, log the provenance after running the command:
::

    provenance log 'motion correction' --new fmri-3dmc.nii --parent fmri.nii 


Publish provenance of known files for subject 'John Doe' as an html file.
::

    provenance report --subject "John Doe" --html


Register a file to the provenance database without inspecting it:
::

    provenance add 'motionvars.mat'

