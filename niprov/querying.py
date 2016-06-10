from collections import namedtuple
QueryField = namedtuple('QueryField', ['name', 'value'])

class Query(object):

    def __init__(self, dependencies):
        self.fields = []
        self.repository = dependencies.getRepository()
        self.cachedResults = None

    def __iter__(self):
        if self.cachedResults is None:
            self.cachedResults = self.repository.inquire(self)
        return self.cachedResults.__iter__()

    def __len__(self):
        if self.cachedResults is None:
            self.cachedResults = self.repository.inquire(self)
        return len(self.cachedResults)

    def getFields(self):
        return self.fields

    def byModality(self, val):
        self.fields.append(QueryField('modality', val))
        return self

    def byProject(self, val):
        self.fields.append(QueryField('project', val))
        return self

    def byUser(self, val):
        self.fields.append(QueryField('user', val))
        return self
