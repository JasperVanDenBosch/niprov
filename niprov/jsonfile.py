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
        self.pictureCache = dependencies.getPictureCache()
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
        self.pictureCache.saveToDisk(for_=image)

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

    def byLocations(self, listOfLocations):
        return [f for f in self.all() if f.location.toString() in listOfLocations]

    def getSeries(self, image):
        """Get the object that carries provenance for the series that the image 
        passed is in. 

        Args:
            image (:class:`.DicomFile`): File that is part of a series.

        Returns:
            :class:`.DicomFile`: Image object that caries provenance for the series.
        """
        seriesId = image.getSeriesId()
        if seriesId is None:
            return None
        for image in self.all():
            if 'seriesuid' in image.provenance and (
                image.provenance['seriesuid'] == seriesId):
                return image

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

    def byParents(self, listOfParentLocations):
        return [f for f in self.all() if set(listOfParentLocations).intersection(
            f.provenance.get('parents',[]))]

    def inquire(self, query):
        field = query.getFields()[0]
        matches = []
        for image in self.all():
            if field.name in image.provenance:
                if field.all:
                    if not image.provenance[field.name] in matches:
                        matches.append(image.provenance[field.name])
                else:
                    if image.provenance[field.name] == field.value:
                        matches.append(image)
        return matches

    def search(self, text):
        fields = ['location','user','subject','project','protocol',
                  'transformation','technique','modality']
        matches = []
        for image in self.all():
            score = 0
            for word in text.split():
                for field in fields:
                    if field in image.provenance:
                        score += image.provenance[field].count(word)
            if score > 0:
                matches.append((image, score))
        sortedResults = sorted(matches, key=itemgetter(1), reverse=True)
        return [i for i, s in sortedResults[:20]]
        

