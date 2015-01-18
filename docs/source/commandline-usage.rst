Commandline Usage
=================

Look for image files below the current directory, inspect them and store the obtained provenance metadata. 
::
    discover .


Add provenance for a new file created as a result of an existing file:
::
    record 'motion correction' fmri.nii fmri-3dmc.nii


Publish provenance of known files for subject 'John Doe' as an html file.
::
    provenance --subject "John Doe" --html

