#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.dependencies import Dependencies


def search(text, dependencies=Dependencies()):
    """
    Search for files with the given text in their provenance fields.

    Args:
        text (str): Words to look for.

    Returns:
        list: List of BaseFile objects
    """
    return dependencies.getRepository().search(text)
