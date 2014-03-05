from . import mongo
import pymongo

from pymongo.errors import OperationFailure

class DatabaseError(object):
	pass

def player_if_exists(name):
	return mongo.db.players.find_one({'name': name})

def players(spec=None, **kwargs):
	return mongo.db.players.find(spec=spec, **kwargs)

def add_player(player):
	try:
		mongo.db.players.insert(player)
	except OperationFailure as e:
		raise DatabaseError

def players_by_rank(spec=None, **kwargs):
	return players(spec, sort=(['rank', 'name'], pymongo.ASCENDING))
	