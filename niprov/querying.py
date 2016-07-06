from collections import namedtuple
QueryField = namedtuple('QueryField', ['name', 'value', 'all'])

class Query(object):

    def __init__(self, dependencies):
        self.fields = []
        self.repository = dependencies.getRepository()
        self.location = dependencies.getLocationFactory()
        self.cachedResults = None

    def __iter__(self):
        if self.cachedResults is None:
            self.cachedResults = self.repository.inquire(self)
        return self.cachedResults.__iter__()

    def __len__(self):
        if self.cachedResults is None:
            self.cachedResults = self.repository.inquire(self)
        return len(self.cachedResults)

    def __contains__(self, key):
        if self.cachedResults is None:
            self.cachedResults = self.repository.inquire(self)
        return key in self.cachedResults

    def _fieldHasValue(self, field, value):
        return QueryField(field, value=value, all=False)

    def _fieldAllValues(self, field):
        return QueryField(field, value=None, all=True)

    def getFields(self):
        return self.fields

    def byLocation(self, val):
        val = self.location.completeString(val)
        return self.repository.byLocation(val)

    def all(self):
        return self.repository.all()

    def latest(self):
        return self.repository.latest()

    def statistics(self):
        return self.repository.statistics()

    def byModality(self, val):
        self.fields.append(self._fieldHasValue('modality', val))
        return self

    def byProject(self, val):
        self.fields.append(self._fieldHasValue('project', val))
        return self

    def byUser(self, val):
        self.fields.append(self._fieldHasValue('user', val))
        return self

    def bySubject(self, val):
        self.fields.append(self._fieldHasValue('subject', val))
        return self

    def byApproval(self, val):
        self.fields.append(self._fieldHasValue('approval', val))
        return self

    def allModalities(self):
        self.fields.append(self._fieldAllValues('modality'))
        return self

    def allProjects(self):
        self.fields.append(self._fieldAllValues('project'))
        return self

    def allUsers(self):
        self.fields.append(self._fieldAllValues('user'))
        return self

    def copiesOf(self, target):
        checksum = target.provenance.get('hash', None)
        filesize = target.provenance.get('size', 0)
        if checksum and filesize > 0:
            self.fields.append(self._fieldHasValue('hash', checksum))
        else:
            self.cachedResults = []
        return self
