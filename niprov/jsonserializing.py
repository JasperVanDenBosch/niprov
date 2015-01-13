#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import copy
from datetime import datetime


class JsonSerializer(object):

    def serialize(self, record):
        flatRecord = copy.deepcopy(record)
        flatRecord['acquired'] = record['acquired'].isoformat()
        return json.dumps(flatRecord)

    def deserialize(self, jsonRecord):
        record = json.loads(jsonRecord)
        isoformat = "%Y-%m-%dT%H:%M:%S.%f"
        record['acquired'] = datetime.strptime(record['acquired'], isoformat)
        return record
