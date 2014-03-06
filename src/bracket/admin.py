from . import app
from . import mongo
from . import db, errors, players

from flask import render_template, url_for, redirect, request

def require_admin(method):
    def _auth_helper():
        # Check for admin
        if False:
            raise errors.AuthenticationError
        method() 
    return _auth_helper


def display_admin_panel():
    sort_order = [('uniqname', db.SORT_ASCENDING)]
    players = db.players(sort=sort_order)
    matches = db.matches(spec={'round': 1})
    return render_template('admin.view', 
        players=players,
        matches=matches
    )

def admin_add_player():
    player_name = request.form.get('name')
    player_rank = request.form.get('rank')
    player_uniqname = request.form.get('uniqname')
    if not player_name or not player_rank or not player_uniqname:
        raise errors.InvalidRequest
    player = db.player_if_exists(player_uniqname)
    if player:
        player['name'] = player_name
        player['rank'] = player_rank
        player['uniqname'] = player_uniqname
        db.update_player(player)
    else:
        player = {
            'name': player_name,
            'rank': player_rank,
            'uniqname': player_uniqname
        }
        db.add_player(player)
    return redirect(url_for('admin'))

@require_admin
@app.route('/admin', methods=['GET'])
def admin():
    return display_admin_panel()

@require_admin
@app.route('/admin/player', methods=['POST'])
def admin_player():
    action = request.form.get('action', '').upper()
    ajax = bool(request.form.get('ajax', False))
    if action not in ADMIN_PLAYER_ACTIONS:
        raise InvalidRequest
    if action == PLAYER_ADD:
        return admin_add_player()
    elif action == PLAYER_EDIT:
        return admin_add_player()
    elif action == PLAYER_REMOVE:
        raise InvalidRequest
    else:
        raise InvalidRequest


