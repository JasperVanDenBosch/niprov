#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest
from mock import Mock
from datetime import datetime
import json
from tests.ditest import DependencyInjectionTestBase


class SerializerTests(DependencyInjectionTestBase):

    def setUp(self):
        super(SerializerTests, self).setUp()
        self.fileFactory.fromProvenance.side_effect = lambda p: self.imageWithProvenance(p)

    def imageWithProvenance(self, prov):
        img = Mock()
        img.provenance = prov
        if 'location' in prov:
            img.location.toString.return_value = prov['location']
        return img

    def test_serialize_makes_time_fields_a_string(self):
        from niprov.jsonserializing import JsonSerializer  
        serializer = JsonSerializer(self.dependencies)
        record = {}
        record['acquired'] = datetime.now()
        record['created'] = datetime.now()
        record['added'] = datetime.now()
        out = serializer.serialize(self.imageWithProvenance(record))
        self.assertEqual(json.loads(out)['acquired'], 
            record['acquired'].isoformat())
        self.assertEqual(json.loads(out)['created'], 
            record['created'].isoformat())

    def test_serialize_makes_args_kwargs_values_strings(self):
        from niprov.jsonserializing import JsonSerializer  
        class CustomType(object):
            pass
        serializer = JsonSerializer(self.dependencies)
        record = {}
        ct1 = CustomType()
        ct2 = CustomType()
        record['args'] = [1.23, ct1]
        record['kwargs'] = {'one':ct2, 'two':4.56}
        out = serializer.serialize(self.imageWithProvenance(record))
        self.assertEqual(json.loads(out)['args'], 
            [1.23, str(ct1)])
        self.assertEqual(json.loads(out)['kwargs'], 
            {'one':str(ct2), 'two':4.56})

    def test_serialize_and_deserialize_dont_balk_if_time_field_absent(self):
        from niprov.jsonserializing import JsonSerializer  
        serializer = JsonSerializer(self.dependencies)
        record = {}
        img1 = self.imageWithProvenance(record)
        jsonrecord = serializer.serialize(img1)
        out = serializer.deserialize(jsonrecord)
        self.assertEqual(img1.provenance, out.provenance)

    def test_deserialize_makes_time_field_a_datetime_object(self):
        from niprov.jsonserializing import JsonSerializer  
        serializer = JsonSerializer(self.dependencies)
        record = {}
        acquired = datetime.now()
        record['acquired'] = acquired.isoformat()      
        created = datetime.now()
        record['created'] = created.isoformat()      
        out = serializer.deserialize(json.dumps(record))
        self.assertEqual(out.provenance['acquired'], acquired)
        self.assertEqual(out.provenance['created'], created)

    def test_serializeList_makes_time_field_a_string(self):
        from niprov.jsonserializing import JsonSerializer  
        serializer = JsonSerializer(self.dependencies)
        record = {}
        record['acquired'] = datetime.now()
        record['created'] = datetime.now()
        out = serializer.serializeList([self.imageWithProvenance(record)])
        self.assertEqual(json.loads(out)[0]['acquired'], 
            record['acquired'].isoformat())
        self.assertEqual(json.loads(out)[0]['created'], 
            record['created'].isoformat())

    def test_swallows_object_ids(self):
        from bson.objectid import ObjectId
        from niprov.jsonserializing import JsonSerializer  
        serializer = JsonSerializer(self.dependencies)
        record = {}
        record['_id'] = ObjectId('564168f2fb481f480891263c')
        out = serializer.serializeList([self.imageWithProvenance(record)])
        self.assertNotIn('_id', json.loads(out)[0])


