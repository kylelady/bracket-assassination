import conn
from .. import errors

mongo = conn.get_dbconnection()

class Player(object):

    def __init__(self, uniqname, full_name, rank=None):
        self.uniqname = uniqname
        self.full_name = full_name
        self.rank = rank

    def to_dict(self):
        obj = {
            'uniqname': self.uniqname,
            'full_name': self.full_name,
        }
        if self.rank:
            obj['rank'] = self.rank
        if self._id:
            obj['_id'] = self._id
        return obj

def save_new(player):
    player_dict = player.to_dict()
    try:
        mongo.players.insert(player_dict)
    except conn.MongoError:
        raise conn.DatabaseError
    return player.to_dict()

def save(player):
    player_dict = player.to_dict()
    doc = { '$set': player_dict }
    try:
        mongo.players.update(spec={'uniqname': uniqname}, doc=doc)
    except conn.MongoError:
        raise conn.DatabaseError
    return player_dict

def from_dict(player_dict):
    uniqname = player_dict['uniqname']
    full_name = player_dict['full_name']
    rank = player_dict.get('rank', None)
    return Player(uniqname,
        full_name,
        rank=rank,
        )

def from_uniqname(uniqname):
    try:
        db_player = mongo.players.find_one(spec={'uniqname', uniqname})
        if db_player:
            return from_dict(db_player)
    except conn.MongoError:
        raise conn.DatabaseError
    return None

def remove_uniqname(uniqname):
    try:
        mongo.players.remove(spec_or_id={'uniqname': uniqname})
    except conn.MongoError:
        raise conn.DatabaseError

def find_many(spec=None, **kwargs):
    try:
        db_players = mongo.players.find(spec=spec, **kwargs)
        players = list()
        for db_player in db_players:
            player = from_dict(db_player)
            players.append(player)
        return players
    except conn.MongoError:
        raise conn.DatabaseError
    return None

    