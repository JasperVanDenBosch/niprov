import os
from niprov import Context
provenance = Context()
(img, s) = provenance.add('testdata/nifti/qt1.nii.gz')
provenance.view(os.path.abspath('testdata/nifti/qt1.nii.gz'))






