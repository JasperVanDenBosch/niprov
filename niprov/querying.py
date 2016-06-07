from collections import namedtuple
QueryField = namedtuple('QueryField', ['name', 'value'])

class Query(object):

    def __init__(self):
        self.fields = []

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
