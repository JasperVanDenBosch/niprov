from __future__ import division
import logging
from datetime import datetime
from functools import partial
from niprov.basefile import BaseFile
from niprov.libraries import Libraries


class FifFile(BaseFile):

    def __init__(self, location, **kwargs):
        super(FifFile, self).__init__(location, **kwargs)
        self.libs = self.dependencies.getLibraries()

    def inspect(self):
        provenance = super(FifFile, self).inspect()
        """ try:
                img = self.libs.mne.io.Raw(self.path, allow_maxshield=True)
                except ValueError:
                    pass
                else:
                    inspect file
                    Return
        """
        ftypes = {
            'cov': self.libs.mne.read_cov,
            'epo': self.libs.mne.read_epochs,
            'ave': self.libs.mne.read_evokeds,
            'fwd': self.libs.mne.read_forward_solution,
            'trans': self.libs.mne.read_trans,
            'raw': partial(self.libs.mne.io.read_raw_fif, allow_maxshield=True),
        }
        oldLevel = logging.getLogger('mne').getEffectiveLevel()
        logging.getLogger('mne').setLevel(logging.ERROR)
        for ftype, readfif in ftypes.items():
            try:
                img = readfif(self.path)
                if img == []:
                    continue
                break
            except ValueError:
                continue
        else:
            ftype = 'other'
        logging.getLogger('mne').setLevel(oldLevel)

        if ftype == 'raw':
            sub = img.info['subject_info']
            if sub is not None:
                provenance['subject'] = sub['first_name']+' '+sub['last_name']
            provenance['project'] = img.info['proj_name']
            acqTS = img.info['meas_date'][0]
            provenance['acquired'] = datetime.fromtimestamp(acqTS)
            T = img.last_samp - img.first_samp + 1
            provenance['dimensions'] = [img.info['nchan'], T]
            provenance['sampling-frequency'] = img.info['sfreq']
            provenance['duration'] = T/img.info['sfreq']

        if ftype == 'epo':
            provenance['lowpass'] = img.info['lowpass']
            provenance['highpass'] = img.info['highpass']
            provenance['bad-channels'] = img.info['bads']
            provenance['dimensions'] = [img.events.shape[0], img.times.shape[0]]

        if ftype == 'ave':
            nEvokeds = len(img)
            provenance['dimensions'] = [nEvokeds] + list(img[0].data.shape)

        if ftype == 'cov':
            provenance['dimensions'] = list(img.data.shape)

        provenance['fif-type'] = ftype
        provenance['modality'] = 'MEG'
        return provenance

    def attach(self, form='json'):
        """
        Attach the current provenance to the file by appending it as a
        json-encoded string to the 'description' header field.

        Args:
            form (str): Data format in which to serialize provenance. Defaults 
                to 'json'.
        """
        info = self.libs.mne.io.read_info(self.path)
        provstr = self.getProvenance(form)
        info['description'] = info['description']+' NIPROV:'+provstr
        self.libs.mne.io.write_info(self.path, info)

