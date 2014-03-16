import web
import db
import errors
import const

import cyclone.web
from  bson.objectid import ObjectId

import db.conn

mongo = db.conn.get_dbconnection()

class SinglePlayerHandler(web.RequestHandler):

    def get(self, uniqname):
        res = dict()
        player = mongo.players.find_one(spec={'uniqname': uniqname})
        res['player'] = player
        self.write_mongo_obj(res)

    def post(self, uniqname):
        raise InvalidRequest

class PlayerDeleteHandler(web.RequestHandler):

    def post(self, uniqname):
        mongo.players.remove(spec_or_id={'uniqname': uniqname})
        self.write({'status': const.STATUS_OK})

class PlayerHandler(web.RequestHandler):

    def get(self):
        res = dict()
        players = mongo.players.find()
        res['players'] = players
        self.write_mongo_obj(res)

    def post(self):
        uniqname = self.get_argument('uniqname')
        full_name = self.get_argument('full_name')
        rank = self.get_argument('rank', None)
        player = {
            'uniqname': uniqname,
            'full_name': full_name,
        }
        if rank:
            player['rank'] = rank
        mongo.players.insert(player)
        self.write_mongo_obj(player)

class MatchHandler(web.RequestHandler):

    def get(self):
        res = dict()
        matches = mongo.matches.find()
        res['matches'] = matches
        self.write_mongo_obj(res)

    def post(self):
        favorite = self.get_argument('favorite')
        underdog = self.get_argument('underdog')
        favorite_id = ObjectId(favorite)
        underdog_id = ObjectId(underdog)
        f = mongo.players.find_one(spec_or_id=favorite_id)
        u = mongo.players.find_one(spec_or_id=underdog_id)
        if not f or not u:
            raise errors.InvalidRequest
        match = {
            'favorite': favorite_id,
            'underdog': underdog_id,
        }
        mongo.matches.insert(match)
        self.write_mongo_obj(match)

class AdminHandler(web.RequestHandler):

    def get(self):
        self.render('admin.view')


