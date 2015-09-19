import pymongo
from niprov.dependencies import Dependencies


class MongoRepository(object):

    def __init__(self, dependencies=Dependencies()):
        self.config = dependencies.getConfiguration()
        self.factory = dependencies.getFileFactory()
        client = pymongo.MongoClient(self.config.database_url)
        self.db = client.get_default_database()

    def byLocation(self, locationString):
        """Get the provenance for a file at the given location. 

        In the case of a dicom series, this returns the provenance for the 
        series.

        Args:
            locationString (str): Location of the image file.

        Returns:
            dict: Provenance for one image file.
        """
        record = self.db.provenance.find_one({'location':locationString})
        return self.factory.fromProvenance(record)

    def knowsByLocation(self, locationString):
        """Whether the file at this location has provenance associated with it.

        Returns:
            bool: True if provenance is available for that path.
        """
        return self.db.provenance.find_one(
            {'location':locationString}) is not None

    def knows(self, image):
        """Whether this file has provenance associated with it.

        Returns:
            bool: True if provenance is available for this image.
        """
        return self.knowsByLocation(image.location.toString())

    def getSeries(self, image):
        """Get the object that carries provenance for the series that the image 
        passed is in. 

        Args:
            image (:class:`.DicomFile`): File that is part of a series.

        Returns:
            :class:`.DicomFile`: Image object that caries provenance for the series.
        """
        seriesUid = image.getSeriesId()
        record = self.db.provenance.find_one({'seriesuid':seriesUid})
        return self.factory.fromProvenance(record)

    def knowsSeries(self, image):
        """Whether this file is part of a series for which provenance 
        is available.

        Args:
            image (:class:`.BaseFile`): File for which the series is sought.

        Returns:
            bool: True if provenance is available for this series.
        """
        seriesUid = image.getSeriesId()
        if seriesUid is None:
            return False
        return self.db.provenance.find_one({'seriesuid':seriesUid}) is not None

    def add(self, image):
        """Add the provenance for one file to storage.

        Args:
            image (:class:`.BaseFile`): Image file to store.
        """
        self.db.provenance.insert_one(image.provenance)

    def update(self, image):
        """Save changed provenance for this file..

        Args:
            image (:class:`.BaseFile`): Image file that has changed.
        """
        self.db.provenance.update({'location':image.location.toString()}, 
            image.provenance)

    def all(self):
        """Retrieve all known provenance from storage.

        Returns:
            list: List of provenance for known files.
        """
        return self.db.provenance.find()


    def bySubject(self, subject):
        """Get the provenance for all files of a given participant. 

        Args:
            subject (str): The name or other ID string.

        Returns:
            list: List of provenance for known files imaging this subject.
        """
        return self.db.provenance.find({'subject':subject})

    def byApproval(self, approvalStatus):
        return self.db.provenance.find({'approval':approvalStatus})

    def updateApproval(self, locationString, approvalStatus):
        self.db.provenance.update({'location':locationString}, 
            {'$set': {'approval': approvalStatus}})



