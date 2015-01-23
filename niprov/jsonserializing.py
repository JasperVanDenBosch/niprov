#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import copy
from datetime import datetime


class JsonSerializer(object):
    """Helper to convert provenance data to and from json encoded strings.
    """

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
        if 'acquired' in record:
            flatRecord['acquired'] = record['acquired'].strftime(isoformat)
        return flatRecord

    def _inflate(self, flatRecord):
        isoformat = "%Y-%m-%dT%H:%M:%S.%f"
        record = flatRecord
        if 'acquired' in flatRecord:
            record['acquired'] = datetime.strptime(record['acquired'], isoformat)
        return record
