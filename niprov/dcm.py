from datetime import datetime
from niprov.basefile import BaseFile
from niprov.dependencies import Dependencies


class DicomFile(BaseFile):

    def __init__(self, fpath, dependencies=Dependencies(), **kwargs):
        super(DicomFile, self).__init__(fpath, **kwargs)
        self.libs = dependencies

    def inspect(self):
        provenance = super(DicomFile, self).inspect()
        try:
            img = self.libs.dicom.read_file(self.path)
        except:
            self.listener.fileError(self.path)
            return provenance
        provenance['subject'] = img.PatientID
        provenance['protocol'] = img.SeriesDescription
        acqstring = img.AcquisitionDateTime.split('.')[0]
        dateformat = '%Y%m%d%H%M%S'
        provenance['acquired'] = datetime.strptime(acqstring,dateformat)
        return provenance
        
