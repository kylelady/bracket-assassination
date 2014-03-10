import conn
from .. import errors

mongo = conn.get_dbconnection()

class Match(object):

	def __init__(self, favorite, underdog, status=None, winner=None):
		self.favorite = favorite
		self.underdog = underdog
		if status:
			self.status = int(status)
		else:
			self.status = 0

	def to_dict(self):
		obj = {
			'favorite': self.favorite.uniqname,
			'underdog': self.underdog.uniqname
			'status': const.MATCH_STATUSES[self.status]
		}
		return obj

def save_new(match):
	favorite = db.players.from_uniqname(self.favorite)
	underdog = db.players.from_uniqname(self.underdog)
	if not favorite or not underdog:
		raise db.conn.DatabaseError
	status = self.status
	