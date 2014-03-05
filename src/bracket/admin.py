from . import app
from . import mongo
from flask import render_template, url_for, redirect
from . import db

class AuthenticationError(object):
	pass

def require_admin(method):
	def _auth_helper():
		# Check for admin
		if False:
			raise AuthenticationError
		method() 
	return _auth_helper


def display_admin_panel():
	return render_template('admin.view')

@require_admin
@app.route('/admin', methods=['GET'])
def admin():
	return display_admin_panel()

@require_admin
@app.route('/admin/player', methods=['POST'])
def admin_add_player():
	player_name = request.form['name']
	player_rank = request.form['rank']
	player = db.player_if_exists(player_name)
	if player:
		player['name'] = player_name
		player['rank'] = player_rank
		db.update_player(player)
	else:
		player = {
			'name': player_name,
			'rank': player_rank,
		}
		db.add_player(player)

