import os
from operator import itemgetter
from niprov.dependencies import Dependencies


class JsonFile(object):
    """Stores provenance in a local text file encoded as json.
    """

    def __init__(self, dependencies=Dependencies()):
        self.filesys = dependencies.getFilesystem()
        self.json = dependencies.getSerializer()
        self.factory = dependencies.getFileFactory()
        url = dependencies.getConfiguration().database_url
        self.datafile = os.path.expanduser(url)

    def add(self, image):
        """Add the provenance for one file to storage.

        Args:
            image (:class:`.BaseFile`): Image file to store.
        """
        current = self._all()
        current.append(image.provenance)
        jsonstr = self.json.serializeList(current)
        self.filesys.write(self.datafile, jsonstr)

    def update(self, image):
        """Save changed provenance for this file..

        Args:
            image (:class:`.BaseFile`): Image file that has changed.
        """
        current = self._all()
        for r in range(len(current)):
            if current[r]['location'] == image.location.toString():
                current[r] = image.provenance
        jsonstr = self.json.serializeList(current)
        self.filesys.write(self.datafile, jsonstr)

    def all(self):
        """Retrieve all known provenance from storage.

        Returns:
            list: List of provenance for known files.
        """
        records = self._all()
        return [self.factory.fromProvenance(record) for record in records]

    def _all(self):
        try:
            jsonstr = self.filesys.read(self.datafile)
        except IOError:
            return []
        return self.json.deserializeList(jsonstr)

    def knowsByLocation(self, locationString):
        """Whether the file at this path has provenance associated with it.

        Returns:
            bool: True if provenance is available for that path.
        """
        try:
            self.byLocation(locationString)
        except IndexError:
            return False
        return True

    def knows(self, image):
        """Whether this file has provenance associated with it.

        Returns:
            bool: True if provenance is available for this image.
        """
        try:
            self.byLocation(image.path)
        except IndexError:
            return False
        return True

    def knowsSeries(self, image):
        """Whether the series that this file is part of has provenance 
        associated with it.

        Args:
            image (:class:`.BaseFile`): File for which the series is sought.

        Returns:
            bool: True if provenance is available for this series.
        """
        try:
            self.getSeries(image)
        except IndexError:
            return False
        return True

    def byLocation(self, locationString):
        """Get the provenance for a file at the given location. 

        In the case of a dicom series, this returns the provenance for the 
        series.

        Args:
            locationString (str): Location of the image file.

        Returns:
            dict: Provenance for one image file.
        """
        for record in self._all():
            if record['location'] == locationString:
                return self.factory.fromProvenance(record)
            elif 'filesInSeries' in record and locationString in record['filesInSeries']:
                return self.factory.fromProvenance(record)
        else:
            raise IndexError('No file with that path known.')

    def bySubject(self, subject):
        """Get the provenance for all files of a given participant. 

        Args:
            subject (str): The name or other ID string.

        Returns:
            list: List of provenance for known files imaging this subject.
        """
        all = self._all()
        recordsWithSubject = [f for f in all if 'subject' in f]
        records = [f for f in recordsWithSubject if f['subject']==subject]
        return [self.factory.fromProvenance(record) for record in records]

    def getSeries(self, image):
        """Get the object that carries provenance for the series that the image 
        passed is in. 

        Args:
            image (:class:`.DicomFile`): File that is part of a series.

        Returns:
            :class:`.DicomFile`: Image object that caries provenance for the series.
        """
        if image.getSeriesId() is None:
            raise IndexError('Image has no series id.')
        seriesId = image.getSeriesId()
        for record in self._all():
            if 'seriesuid' in record and record['seriesuid'] == seriesId:
                return self.factory.fromProvenance(record)
        else:
            raise IndexError('No provenance record for that series.')

    def byApproval(self, approvalStatus):
        allRecords = self._all()
        matches = []
        for prov in allRecords:
            if 'approval' in prov:
                if prov['approval'] == approvalStatus:
                    matches.append(prov)
        return [self.factory.fromProvenance(r) for r in matches]

    def updateApproval(self, fpath, approvalStatus):
        img = self.byLocation(fpath)
        img.provenance['approval'] = approvalStatus
        self.update(img)

    def latest(self, n=20):
        allRecords = self._all()
        sortedRecords = sorted(allRecords, key=itemgetter('added'), reverse=True)
        records = sortedRecords[:n]
        return [self.factory.fromProvenance(record) for record in records]

    def statistics(self):
        stats = {}
        allRecords = self._all()
        stats['count'] = len(allRecords)
        stats['totalsize'] = sum([r['size'] for r in allRecords])
        return stats

    def byId(self, uid):
        for record in self._all():
            if record['id'] == uid:
                return self.factory.fromProvenance(record)
        else:
            raise IndexError('No file with that path known.')

       

