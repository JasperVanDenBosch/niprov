import json, copy
from datetime import datetime
from niprov.format import Format


class JsonFormat(Format):
    """Helper to convert provenance data to and from json encoded strings.
    """

    def __init__(self, dependencies):
        super(JsonFormat, self).__init__(dependencies)
        self.fileExtension = 'json'
        self.file = dependencies.getFileFactory()

    def serializeSingle(self, record):
        """
        Convert one provenance item from its native python dict type to
        a json string.

        Args:
            record (dict): The provenance item to convert.

        Returns:
            str: Json version of the provenance.
        """
        flat = self._deflate(record.provenance)
        return json.dumps(flat, cls=DateTimeAwareJSONEncoder)

    def deserialize(self, jsonRecord):
        """
        Convert one provenance item from its json string version to the 
        native python dictionary format.

        Args:
            jsonRecord (str): The provenance item to convert as json-encoded 
                string.

        Returns:
            dict: Python dictionary of the provenance.
        """
        provenance = json.loads(jsonRecord, cls=DateTimeAwareJSONDecoder)
        return self.file.fromProvenance(provenance)

    def serializeList(self, listOfRecords):
        """
        Convert a list of provenance items from its native list of python dict 
        type to a json string.

        Args:
            listOfRecords (list): The provenance items to convert.

        Returns:
            str: Json version of the provenance items.
        """
        flatRecords = [self._deflate(r.provenance) for r in listOfRecords]
        return json.dumps(flatRecords, cls=DateTimeAwareJSONEncoder)

    def deserializeList(self, jsonListOfRecords):
        """
        Convert a list of provenance items from its json string version to the 
        a list of the native python dictionary format.

        Args:
            jsonListOfRecords (str): The provenance items to convert as 
                json-encoded string.

        Returns:
            list: Python list of dictionaries of the provenance.
        """
        provenanceList = json.loads(jsonListOfRecords, cls=DateTimeAwareJSONDecoder)
        return [self.file.fromProvenance(p) for p in provenanceList]

    def _deflate(self, record):
        flatRecord = copy.deepcopy(record)
        def deflateOne(prov):
            if 'args' in prov:
                prov['args'] = [self._strcust(a) for a in prov['args']]
            if 'kwargs' in prov:
                kwargs = prov['kwargs']
                prov['kwargs'] = {k: self._strcust(kwargs[k]) 
                    for k in kwargs.keys()}
            if '_id' in prov:
                del prov['_id']
            return prov
        deflateOne(flatRecord)
        for version in flatRecord.get('_versions', []):
            deflateOne(version)
        return flatRecord

    def _strcust(self, val):
        """Stringify an object that is not of a simple type."""
        if not isinstance(val, (str, unicode, int, float, bool, type(None))):
            return str(val)
        return val

# Taken from http://taketwoprogramming.blogspot.com/2009/06/subclassing-jsonencoder-and-jsondecoder.html

class DateTimeAwareJSONEncoder(json.JSONEncoder):
    """ 
    Converts a python object, where datetime and timedelta objects are converted
    into objects that can be decoded using the DateTimeAwareJSONDecoder.
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                '__type__' : 'datetime',
                'year' : obj.year,
                'month' : obj.month,
                'day' : obj.day,
                'hour' : obj.hour,
                'minute' : obj.minute,
                'second' : obj.second,
                'microsecond' : obj.microsecond,
            }

        else:
            return json.JSONEncoder.default(self, obj)

class DateTimeAwareJSONDecoder(json.JSONDecoder):
    """ 
    Converts a json string, where datetime and timedelta objects were converted
    into objects using the DateTimeAwareJSONEncoder, back into a python object.
    """

    def __init__(self, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        if '__type__' not in d:
            return d

        type = d.pop('__type__')
        if type == 'datetime':
            return datetime(**d)
        else:
            # Oops... better put this back together.
            d['__type__'] = type
            return d
