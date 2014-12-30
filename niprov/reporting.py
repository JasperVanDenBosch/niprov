#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.jsonfile import JsonFile


def report(forFile=None, forSubject=None, repository=JsonFile()):
    if forFile:
        return repository.byPath(forFile)
    elif forSubject:
        return repository.bySubject(forSubject)
    return repository.all()
