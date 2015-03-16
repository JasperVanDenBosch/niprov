from datetime import datetime
from niprov.basefile import BaseFile
from niprov.dependencies import Dependencies


class NiftiFile(BaseFile):

    def __init__(self, fpath, dependencies=Dependencies(), **kwargs):
        super(NiftiFile, self).__init__(fpath, **kwargs)
        self.libs = dependencies

    def attach(self):
        """
        Attach the current provenance to the file by injecting it as a 
        json-encoded extension to the nifti header.
        """
        img = self.libs.nibabel.load(self.path)
        provstr = self.serializer.serialize(self.provenance)
        ext = self.libs.nibabel.nifti1.Nifti1Extension('comment', provstr)
        hdr = img.get_header()
        hdr.extensions.append(ext)
        img.to_filename(self.path)
