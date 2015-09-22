#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import copy
from datetime import datetime


class JsonSerializer(object):
    """Helper to convert provenance data to and from json encoded strings.
    """

    datetimeFields = ['acquired','created','added']

    def serialize(self, record):
        """
        Convert one provenance item from its native python dict type to
        a json string.

        Args:
            record (dict): The provenance item to convert.

        Returns:
            str: Json version of the provenance.
        """
        return json.dumps(self._deflate(record))

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
        return self._inflate(json.loads(jsonRecord))

    def serializeList(self, listOfRecords):
        """
        Convert a list of provenance items from its native list of python dict 
        type to a json string.

        Args:
            listOfRecords (list): The provenance items to convert.

        Returns:
            str: Json version of the provenance items.
        """
        flatRecords = [self._deflate(r) for r in listOfRecords]
        return json.dumps(flatRecords)

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
        flatRecords = json.loads(jsonListOfRecords)
        return [self._inflate(r) for r in flatRecords]

    def _deflate(self, record):
        isoformat = "%Y-%m-%dT%H:%M:%S.%f"
        flatRecord = copy.deepcopy(record)
        for field in self.datetimeFields:
            if field in record:
                flatRecord[field] = record[field].strftime(isoformat)
        if 'args' in record:
            flatRecord['args'] = [self._strcust(a) for a in record['args']]
        if 'kwargs' in record:
            kwargs = record['kwargs']
            flatRecord['kwargs'] = {k: self._strcust(kwargs[k]) 
                for k in kwargs.keys()}
        return flatRecord

    def _inflate(self, flatRecord):
        isoformat = "%Y-%m-%dT%H:%M:%S.%f"
        record = flatRecord
        for field in self.datetimeFields:
            if field in record:
                record[field] = datetime.strptime(record[field], isoformat)
        return record

    def _strcust(self, val):
        """Stringify an object that is not of a simple type."""
        if not isinstance(val, (str, unicode, int, float, bool, type(None))):
            return str(val)
        return val
