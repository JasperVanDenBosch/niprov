#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.dependencies import Dependencies


def inspect(fpath, dependencies=Dependencies()):
    fileFactory = dependencies.getFileFactory()
    return fileFactory.locatedAt(fpath).inspect()


