from datetime import datetime
from niprov.basefile import BaseFile
from niprov.dependencies import Dependencies


class ParrecFile(BaseFile):

    def __init__(self, fpath, dependencies=Dependencies(), **kwargs):
        super(ParrecFile, self).__init__(fpath, **kwargs)
        self.libs = dependencies

    def inspect(self):
        provenance = super(ParrecFile, self).inspect()
        try:
            img = self.libs.nibabel.load(self.path)
        except:
            self.listener.fileError(self.path)
            return provenance
        provenance['subject'] = img.header.general_info['patient_name']
        provenance['protocol'] = img.header.general_info['protocol_name']
        acqstring = img.header.general_info['exam_date']
        dateformat = '%Y.%m.%d / %H:%M:%S'
        provenance['acquired'] = datetime.strptime(acqstring, dateformat)
        return provenance
