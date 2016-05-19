from niprov import Context
provenance = Context()
(img, s) = provenance.add('testdata/nifti/qt1.nii.gz')

import niprov.viewer

niprov.viewer.view(img)






