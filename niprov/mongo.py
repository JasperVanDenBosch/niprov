import pymongo, copy, bson
from niprov.dependencies import Dependencies


class MongoRepository(object):

    def __init__(self, dependencies=Dependencies()):
        self.config = dependencies.getConfiguration()
        self.factory = dependencies.getFileFactory()
        self.pictures = dependencies.getPictureCache()
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
        return self.inflate(record)

    def byLocations(self, listOfLocations):
        records = self.db.provenance.find({'location':{'$in':listOfLocations}})
        return [self.inflate(record) for record in records]

    def getSeries(self, image):
        """Get the object that carries provenance for the series that the image 
        passed is in. 

        Args:
            image (:class:`.DicomFile`): File that is part of a series.

        Returns:
            :class:`.DicomFile`: Image object that caries provenance for 
                         the series.
        """
        seriesUid = image.getSeriesId()
        if seriesUid is None:
            return None
        record = self.db.provenance.find_one({'seriesuid':seriesUid})
        return self.inflate(record)

    def add(self, image):
        """Add the provenance for one file to storage.

        Args:
            image (:class:`.BaseFile`): Image file to store.
        """
        self.db.provenance.insert_one(self.deflate(image))

    def update(self, image):
        """Save changed provenance for this file..

        Args:
            image (:class:`.BaseFile`): Image file that has changed.
        """
        self.db.provenance.update({'location':image.location.toString()}, 
            self.deflate(image))

    def updateApproval(self, locationString, approvalStatus):
        self.db.provenance.update({'location':locationString}, 
            {'$set': {'approval': approvalStatus}})

    def all(self):
        """Retrieve all known provenance from storage.

        Returns:
            list: List of provenance for known files.
        """
        records = self.db.provenance.find()
        return [self.inflate(record) for record in records]

    def latest(self):
        records = self.db.provenance.find().sort('added', -1).limit(20)
        return [self.inflate(record) for record in records]

    def statistics(self):
        grps = self.db.provenance.aggregate(
           [{'$group':
                 {
                   '_id': None,
                   'totalsize': { '$sum': '$size' },
                   'count': { '$sum': 1 }
                 }
            }])
        groups = list(grps)
        if len(list(groups)) == 0:
            return {'count':0}
        return list(groups)[0]

    def byId(self, uid):
        record = self.db.provenance.find_one({'id':uid})
        return self.inflate(record)

    def byParents(self, listOfParentLocations):
        records = self.db.provenance.find({'parents':{
            '$in':listOfParentLocations}})
        return [self.inflate(record) for record in records]

    def inquire(self, query):
        field = query.getFields()[0]
        if field.all:
            records = self.db.provenance.distinct(field.name)
            return records
        else:
            records = self.db.provenance.find({field.name:field.value})
            return [self.inflate(record) for record in records]

    def search(self, text):
        searchfields = ['location','user','subject','project','protocol',
                  'transformation','technique','modality']
        indexspec = [(field, pymongo.TEXT) for field in searchfields]
        self.db.provenance.create_index(indexspec, name='textsearch')
        records = self.db.provenance.find({'$text':{'$search': text}})
        return [self.inflate(record) for record in records]

    def deflate(self, img):
        record = copy.deepcopy(img.provenance)
        snapshotData = self.pictures.getBytes(for_=img)
        if snapshotData:
            record['_snapshot-data'] = bson.Binary(snapshotData)
        return record

    def inflate(self, record):
        if record is None:
            return None
        img = self.factory.fromProvenance(record)
        if '_snapshot-data' in record:
            self.pictures.keep(record['_snapshot-data'], for_=img)
        return img

