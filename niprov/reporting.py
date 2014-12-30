#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.jsonfile import JsonFile


def report(repository=JsonFile()):
    return repository.all()
