import web
import db
import errors

import cyclone.web

from db.players import Player

class SinglePlayerHandler(cyclone.web.RequestHandler):

    def get(self, uniqname):
        player = db.players.from_uniqname(uniqname)
        if player:
            res = self.write(player.to_dict())
        else:
            res = self.write(list())

    @web.require_admin
    def post(self, uniqname):
        raise InvalidRequest

class PlayerDeleteHandler(cyclone.web.RequestHandler):

    def post(self, uniqname):
        db.players.remove_uniqname(uniqname)
        self.write({'status': 'OK'})

class PlayerHandler(cyclone.web.RequestHandler):

    def get(self):
        players = map(lambda p: p.to_dict(), db.players.find_many())
        self.write({'players': players})

    def post(self):
        uniqname = self.get_argument('uniqname')
        full_name = self.get_argument('full_name')
        rank = self.get_argument('rank', None)
        player = Player(uniqname, full_name, rank=rank)
        player_dict = db.players.save_new(player)
        self.write(player_dict)

class AdminHandler(cyclone.web.RequestHandler):

    def get(self):
        self.render('admin.view')



