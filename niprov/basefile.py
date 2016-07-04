import copy
from niprov.dependencies import Dependencies
import niprov.comparing


class BaseFile(object):

    def __init__(self, location, provenance=None, dependencies=Dependencies()):
        self.dependencies = dependencies
        self.listener = dependencies.getListener()
        self.filesystem = dependencies.getFilesystem()
        self.hasher = dependencies.getHasher()
        self.location = dependencies.getLocationFactory().fromString(location)
        self.formats = dependencies.getFormatFactory()
        self.pictures = dependencies.getPictureCache()
        if provenance:
            self.provenance = provenance
        else:
            self.provenance = {}
        self.provenance.update(self.location.toDictionary())
        self.path = self.provenance['path']
        self.status = 'new'

    def inspect(self):
        self.provenance['size'] = self.filesystem.getsize(self.path)
        self.provenance['created'] = self.filesystem.getctime(self.path)
        self.provenance['hash'] = self.hasher.digest(self.path)
        if not 'modality' in self.provenance:
            self.provenance['modality'] = 'other'
        return self.provenance

    def attach(self, form='json'):
        """
        Not implemented for BaseFile parent class.

        Args:
            form (str): Data format in which to serialize provenance. Defaults 
                to 'json'.
        """
        pass

    def getProvenance(self, form='dict'):
        return self.formats.create(form).serialize(self)

    def getSeriesId(self):
        pass

    @property
    def parents(self):
        return self.provenance.get('parents', [])

    @property
    def versions(self):
        return self.provenance.get('_versions', [])

    def compare(self, other):
        return niprov.comparing.compare(self, other, self.dependencies)

    def getProtocolFields(self):
        return None

    def viewSnapshot(self):
        viewer = self.dependencies.getMediumFactory().create('viewer')
        snapshot = self.pictures.getFilepath(for_=self)
        viewer.export(snapshot)

    def getSnapshotFilepath(self):
        return self.pictures.getFilepath(for_=self)

    def keepVersionsFromPrevious(self, previous):
        history = previous.provenance.get('_versions', [])
        prevprov = copy.copy(previous.provenance)
        if '_versions' in prevprov:
            del prevprov['_versions']
        history.append(prevprov)
        self.provenance['_versions'] = history
        self.status = 'new-version'

