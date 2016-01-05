from datetime import datetime
from niprov.basefile import BaseFile
from niprov.libraries import Libraries


class NiftiFile(BaseFile):

    def __init__(self, location, **kwargs):
        super(NiftiFile, self).__init__(location, **kwargs)
        self.libs = self.dependencies.getLibraries()

    def attach(self, form='json'):
        """
        Attach the current provenance to the file by injecting it as a 
        json-encoded extension to the nifti header.

        Args:
            form (str): Data format in which to serialize provenance. Defaults 
                to 'json'.
        """
        img = self.libs.nibabel.load(self.path)
        provstr = self.getProvenance(form)
        ext = self.libs.nibabel.nifti1.Nifti1Extension('comment', provstr)
        hdr = img.get_header()
        hdr.extensions.append(ext)
        img.to_filename(self.path)
