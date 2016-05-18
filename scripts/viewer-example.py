from niprov import Context
provenance = Context()
(img, s) = provenance.add('testdata/dicom/T1.dcm')

import niprov.viewer

niprov.viewer.view(img)

# img.view()        # show in window and return
# img.snapshot()    # save png to cwd




