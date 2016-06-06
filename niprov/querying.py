from collections import namedtuple
QueryField = namedtuple('QueryField', ['name', 'value'])

class Query(object):

    fields = []

    def byModality(self, val):
        self.fields.append(QueryField('modality', val))
        return self

    def getFields(self):
        return self.fields
