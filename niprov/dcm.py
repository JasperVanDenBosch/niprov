from datetime import datetime, time
from niprov.basefile import BaseFile
from niprov.libraries import Libraries


class DicomFile(BaseFile):

    def __init__(self, location, **kwargs):
        super(DicomFile, self).__init__(location, **kwargs)
        self.libs = self.dependencies.getLibraries()

    def inspect(self):
        """
        Inspect the DICOM file attributes.

        If a general AcquisitionDateTime attribute is not present, the 
        SeriesDate and SeriesTime will be used to set the :ref:`field-acquired` 
        provenance field.

        Returns:
            dict: Provenance for the inspected file.
        """
        super(DicomFile, self).inspect()
        img = self.libs.dicom.read_file(self.path)
        self.provenance['subject'] = img.PatientID
        self.provenance['protocol'] = img.SeriesDescription
        self.provenance['seriesuid'] = img.SeriesInstanceUID
        self.provenance['filesInSeries'] = [self.path]
        if hasattr(img, 'NumberOfFrames'):
            self.provenance['multiframeDicom'] = True
            nframes = int(img.NumberOfFrames)
        else:
            self.provenance['multiframeDicom'] = False
            nframes = len(self.provenance['filesInSeries'])
        if hasattr(img, 'Rows'):
            self.provenance['dimensions'] = [int(img.Rows), int(img.Columns), 
                nframes]
        if hasattr(img, 'AcquisitionDateTime'):
            acqstring = img.AcquisitionDateTime.split('.')[0]
            dateformat = '%Y%m%d%H%M%S'
            self.provenance['acquired'] = datetime.strptime(acqstring,dateformat)
        else:
            dateformat = '%Y%m%d'
            acqdate = datetime.strptime(img.SeriesDate, dateformat)
            acqtime = datetime.fromtimestamp(float(img.SeriesTime)).time()
            combined = datetime.combine(acqdate, acqtime)
            self.provenance['acquired'] = combined.replace(microsecond=0)
        return self.provenance


    def getSeriesId(self):
        """
        Return the DICOM "SeriesInstanceUID" that all files in this series 
        have in common.

        Returns:
            str: A string uniquely identifying files belonging to this series.
        """
        if not 'seriesuid' in self.provenance:
            self.inspect()
        return self.provenance['seriesuid']

    def addFile(self, img):
        """
        Add a single DICOM file object to this series.

        The file will be stored in provenance in the 'filesInSeries' list.
        """
        self.provenance['filesInSeries'].append(img.path)
        self._updateNfilesDependentFields()

    def _updateNfilesDependentFields(self):
        if (not self.provenance['multiframeDicom']) and 'dimensions' in self.provenance:
            nfiles = len(self.provenance['filesInSeries'])
            self.provenance['dimensions'][2] = nfiles
        
        
