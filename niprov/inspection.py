#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.dependencies import Dependencies


def inspect(location, dependencies=Dependencies()):
    fileFactory = dependencies.getFileFactory()
    return fileFactory.locatedAt(location).inspect()


