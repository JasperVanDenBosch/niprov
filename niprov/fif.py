from datetime import datetime
from niprov.basefile import BaseFile
from niprov.dependencies import Dependencies


class FifFile(BaseFile):

    def __init__(self, fpath, dependencies=Dependencies(), **kwargs):
        super(FifFile, self).__init__(fpath, **kwargs)
        self.libs = dependencies

    def inspect(self):
        provenance = super(FifFile, self).inspect()
        try:
            img = self.libs.mne.io.Raw(self.path, allow_maxshield=True)
        except:
            self.listener.fileError(self.path)
            return provenance
        subject = img.info['subject_info']
        provenance['subject'] = subject['first_name']+' '+subject['last_name']
        provenance['project'] = img.info['proj_name']
        acqTS = img.info['meas_date'][0]
        provenance['acquired'] = datetime.fromtimestamp(acqTS)
        return provenance

