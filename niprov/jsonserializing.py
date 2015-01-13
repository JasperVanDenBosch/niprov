#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import copy
from datetime import datetime


class JsonSerializer(object):
    """Helper to convert provenance data to and from json encoded strings.
    """

    def serialize(self, record):
        """Convert one provenance item from its native python dict type to
            a json string.

        Args:
            record (dict): The provenance item to convert.

        Returns:
            str: Json version of the provenance.
        """
        return json.dumps(self._deflate(record))

    def deserialize(self, jsonRecord):
        """Convert one provenance item from its json string version to the 
            native python dictionary format.

        Args:
            jsonRecord (str): The provenance item to convert as json-encoded 
                string.

        Returns:
            dict: Python dictionary of the provenance.
        """
        return self._inflate(json.loads(jsonRecord))

    def _deflate(self, record):
        flatRecord = copy.deepcopy(record)
        flatRecord['acquired'] = record['acquired'].isoformat()
        return flatRecord

    def _inflate(self, flatRecord):
        isoformat = "%Y-%m-%dT%H:%M:%S.%f"
        record = flatRecord
        record['acquired'] = datetime.strptime(record['acquired'], isoformat)
        return record
