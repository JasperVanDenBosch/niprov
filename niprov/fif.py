from datetime import datetime
from niprov.basefile import BaseFile
from niprov.dependencies import Dependencies


class FifFile(BaseFile):

    def __init__(self, fpath, dependencies=Dependencies(), **kwargs):
        super(FifFile, self).__init__(fpath, **kwargs)
        self.libs = dependencies

    def inspect(self):
        provenance = super(FifFile, self).inspect()
        img = self.libs.mne.io.Raw(self.path, allow_maxshield=True)
        sub = img.info['subject_info']
        if sub is not None:
            provenance['subject'] = sub['first_name']+' '+sub['last_name']
        provenance['project'] = img.info['proj_name']
        acqTS = img.info['meas_date'][0]
        provenance['acquired'] = datetime.fromtimestamp(acqTS)
        T = img.last_samp - img.first_samp + 1
        provenance['dimensions'] = [img.info['nchan'], T]
        return provenance

