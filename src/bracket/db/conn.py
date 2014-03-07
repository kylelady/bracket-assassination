import pymongo
import pymongo.errors
from .. import errors

import os

MongoError = pymongo.errors.OperationFailure

class DatabaseError(errors.AssassinationException):
    pass

class MongoConf:

    CONNECTION = None

    def __init__(self, host, port):
        self.host = host
        self.port = port

    @classmethod
    def from_environment(cls):
        host = os.environ.get('MONGO_HOST', 'localhost')
        port = os.environ.get('MONGO_PORT', 27017)
        return MongoConf(host, port)

def connect():
    conf = MongoConf.from_environment()
    MongoConf.CONNECTION = pymongo.MongoClient(conf.host, conf.port)
    MongoConf._connected = True

def get_dbconnection():
    if not MongoConf.CONNECTION:
        connect()
    return MongoConf.CONNECTION.nerf


