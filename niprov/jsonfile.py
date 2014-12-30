import json


class JsonFile(object):

    def store(self, provenance):
        with open('provenance.json', 'w') as fp:
            json.dump(provenance, fp, default=datetime2json)

    def all(self):
        with open('provenance.json', 'r') as fp:
            provenance = json.load(fp)
        return provenance


def datetime2json(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj
