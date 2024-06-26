#!/usr/bin/python3
"""This module instantiates an object of DBstorage or FileStorage"""

from os import environ

if environ['HBNB_TYPE_STORAGE'] == 'db':
    from models.engine.db_storage import DBstorage
    storage = DBstorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
