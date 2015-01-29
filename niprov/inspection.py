#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.files import FileFactory


def inspect(fpath, file=FileFactory()):
    return file.locatedAt(fpath).inspect()


