import web
import db
import errors

from db.players import Player

class SinglePlayerHandler(web.ApiHandler):

    def handle_get(self, uniqname):
        player = db.players.from_uniqname(uniqname)
        if player:
            res = self.make_response(player.to_dict())
        else:
            res = self.make_response(list())

    @web.require_admin
    def handle_post(self, uniqname):
        raise InvalidRequest

class PlayerDeleteHandler(web.ApiHandler):

    @web.require_admin
    def handle_post(self, uniqname):
        db.players.remove_uniqname(uniqname)
        self.make_response()



class PlayerHandler(web.ApiHandler):

    def handle_get(self):
        players = map(lambda p: p.to_dict(), db.players.find_many())
        self.make_response(players)

    def handle_post(self):
        uniqname = self.get_argument('uniqname')
        full_name = self.get_argument('full_name')
        rank = self.get_argument('rank', None)
        player = Player(uniqname, full_name, rank=rank)
        player_dict = db.players.save_new(player)
        self.make_response(player_dict)

class AdminHandler(web.AssassinationHandler):

    def handle_get(self):
        self.render('admin.view')



