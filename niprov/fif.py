from datetime import datetime
from niprov.basefile import BaseFile
from niprov.libraries import Libraries


class FifFile(BaseFile):

    def __init__(self, location, **kwargs):
        super(FifFile, self).__init__(location, **kwargs)
        self.libs = self.dependencies.getLibraries()

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

    def attach(self):
        """
        Attach the current provenance to the file by appending it as a
        json-encoded string to the 'description' header field.
        """
        info = self.libs.mne.io.read_info(self.path)
        provstr = self.serializer.serialize(self.provenance)
        info['description'] = info['description']+' NIPROV:'+provstr
        self.libs.mne.io.write_info(self.path, info)

