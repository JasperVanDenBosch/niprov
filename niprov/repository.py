

class Repository(object):

    def byLocation(self, locationString):
        """Get the provenance for a file at the given location. 

        In the case of a dicom series, this returns the provenance for the 
        series.

        Args:
            locationString (str): Location of the image file.

        Returns:
            dict: Provenance for one image file.
        """

    def knowsByLocation(self, locationString):
        """Whether the file at this location has provenance associated with it.

        Returns:
            bool: True if provenance is available for that path.
        """

    def knows(self, image):
        """Whether this file has provenance associated with it.

        Returns:
            bool: True if provenance is available for this image.
        """

    def getSeries(self, image):
        """Get the object that carries provenance for the series that the image 
        passed is in. 

        Args:
            image (:class:`.DicomFile`): File that is part of a series.

        Returns:
            :class:`.DicomFile`: Image object that caries provenance for the series.
        """

    def knowsSeries(self, image):
        """Whether this file is part of a series for which provenance 
        is available.

        Args:
            image (:class:`.BaseFile`): File for which the series is sought.

        Returns:
            bool: True if provenance is available for this series.
        """

    def add(self, image):
        """Add the provenance for one file to storage.

        Args:
            image (:class:`.BaseFile`): Image file to store.
        """

    def update(self, image):
        """Save changed provenance for this file..

        Args:
            image (:class:`.BaseFile`): Image file that has changed.
        """

    def all(self):
        """Retrieve all known provenance from storage.

        Returns:
            list: List of provenance for known files.
        """

    def bySubject(self, subject):
        """Get the provenance for all files of a given participant. 

        Args:
            subject (str): The name or other ID string.

        Returns:
            list: List of provenance for known files imaging this subject.
        """

    def byApproval(self, approvalStatus):
        """"""

    def updateApproval(self, locationString, approvalStatus):
        """"""

    def latest(self, n=20):
        """Get the images that have been registered last. 

        Args:
            n (int): The number of files to retrieve. Defaults to 20.

        Returns:
            list: List of BaseFile objects.
        """

    def byId(self, uid):
        """Get the provenance for a file with the given id. 

        Args:
            uid (str): Unique id for the file.

        Returns:
            BaseFile: File with the given id.
        """
