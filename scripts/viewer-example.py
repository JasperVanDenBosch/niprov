import os
from niprov import ProvenanceContext
provenance = ProvenanceContext()
img = provenance.add('testdata/nifti/qt1.nii.gz')
provenance.view(os.path.abspath('testdata/nifti/qt1.nii.gz'))
img.viewSnapshot()
