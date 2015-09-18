from datetime import datetime
from niprov.basefile import BaseFile
from niprov.libraries import Libraries


class ParrecFile(BaseFile):

    def __init__(self, location, **kwargs):
        super(ParrecFile, self).__init__(location, **kwargs)
        self.libs = self.dependencies.getLibraries()

    def inspect(self):
        provenance = super(ParrecFile, self).inspect()
        img = self.libs.nibabel.load(self.path)
        provenance['subject'] = img.header.general_info['patient_name']
        provenance['protocol'] = img.header.general_info['protocol_name']
        acqstring = img.header.general_info['exam_date']
        dateformat = '%Y.%m.%d / %H:%M:%S'
        provenance['acquired'] = datetime.strptime(acqstring, dateformat)
        provenance['dimensions'] = list(img.shape)
        return provenance
