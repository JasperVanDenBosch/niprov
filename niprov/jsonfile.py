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

    def serializeAndWrite(self, images):
        jsonstr = self.json.serializeList(images)
        self.filesys.write(self.datafile, jsonstr)

    def add(self, image):
        """Add the provenance for one file to storage.

        Args:
            image (:class:`.BaseFile`): Image file to store.
        """
        current = self.all()
        current.append(image)
        self.serializeAndWrite(current)

    def update(self, image):
        """Save changed provenance for this file..

        Args:
            image (:class:`.BaseFile`): Image file that has changed.
        """
        current = self.all()
        for r in range(len(current)):
            if current[r].location.toString() == image.location.toString():
                current[r] = image
        self.serializeAndWrite(current)

    def all(self):
        """Retrieve all known provenance from storage.

        Returns:
            list: List of provenance for known files.
        """
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
        for image in self.all():
            if image.location.toString() == locationString:
                return image
            elif 'filesInSeries' in image.provenance and (
                locationString in image.provenance['filesInSeries']):
                return image
        else:
            raise IndexError('No file with that path known.')

    def byLocations(self, listOfLocations):
        return [f for f in self.all() if f.location.toString() in listOfLocations]

    def bySubject(self, subject):
        """Get the provenance for all files of a given participant. 

        Args:
            subject (str): The name or other ID string.

        Returns:
            list: List of provenance for known files imaging this subject.
        """
        all = self.all()
        imagesWithSubject = [f for f in all if 'subject' in f.provenance]
        return [f for f in imagesWithSubject if f.provenance['subject']==subject]

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
        for image in self.all():
            if 'seriesuid' in image.provenance and (
                image.provenance['seriesuid'] == seriesId):
                return image
        else:
            raise IndexError('No provenance record for that series.')

    def byApproval(self, approvalStatus):
        matches = []
        for image in self.all():
            if 'approval' in image.provenance:
                if image.provenance['approval'] == approvalStatus:
                    matches.append(image)
        return matches

    def updateApproval(self, fpath, approvalStatus):
        img = self.byLocation(fpath)
        img.provenance['approval'] = approvalStatus
        self.update(img)

    def latest(self, n=20):
        def dateTimeAdded(img):
            return img.provenance.get('added')
        sortedImages = sorted(self.all(), key=dateTimeAdded, reverse=True)
        return sortedImages[:n]

    def statistics(self):
        stats = {}
        images = self.all()
        stats['count'] = len(images)
        sizes = [img.provenance['size'] for img in images if 'size' in img.provenance]
        stats['totalsize'] = sum(sizes)
        return stats

    def byId(self, uid):
        for image in self.all():
            if image.provenance['id'] == uid:
                return image
        else:
            raise IndexError('No file with that path known.')

    def byParents(self, listOfParentLocations):
        return [f for f in self.all() if set(listOfParentLocations).intersection(
            f.provenance.get('parents',[]))]

       

