from . import mongo
from . import errors

import pymongo

from pymongo.errors import OperationFailure

SORT_ASCENDING = pymongo.ASCENDING

def player_if_exists(uniqname):
    try:
        return mongo.db.players.find_one({'uniqname': uniqname})
    except OperationFailure:
        raise errors.DatabaseError

def players(spec=None, **kwargs):
    try:
        return mongo.db.players.find(spec=spec, **kwargs)
    except OperationFailure:
        raise errors.DatabaseError

def add_player(player):
    try:
        return mongo.db.players.insert(player)
    except OperationFailure:
        raise errors.DatabaseError

def update_player(spec, change, **kwargs):
    try:
        doc = { '$set': change }
        return mongo.db.players.update(spec, doc, **kwargs)
    except OperationFailure:
        raise errors.DatabaseError

def players_by_rank(spec=None, **kwargs):
    sort_order = [
        ('rank', SORT_ASCENDING),
        ('name', SORT_ASCENDING),
        ('uniqname', SORT_ASCENDING),
    ]
    return players(spec, sort=sort_order, **kwargs)

def matches(spec=None, **kwargs):
    try:
        return mongo.db.matches.find(spec=spec, **kwargs)
    except OperationFailure:
        raise error.DatabaseError

    