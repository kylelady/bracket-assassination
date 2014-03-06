from . import app
from . import mongo
from . import errors, db

import json

import bson.json_util
from flask import request

PLAYER_FIELDS = [ 'name', 'uniqname', 'rank']

PLAYER_FIELDS_DICT = { 
    '_id': False,
    'name': True,
    'uniqname': True, 
    'rank': True,
}


def enforce_present(get_args=None, post_args=None):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            if request.method == 'GET' and get_args:
                arg_container = request.args
            elif request.method == 'POST' and post_args:
                arg_container = request.form
            else:
                # No mandatory args, just make an empty list
                arg_container = list()
            # Look for all the mandatory args
            for arg in arg_container:
                if arg not in request.args:
                    raise errors.InvalidRequest
            # All were found, call function
            function(*args, **kwargs)
        return wrapper
    return real_decorator

@app.route('/api/players')
def json_players():
    fields = set(request.args) & set(PLAYER_FIELDS)
    spec = { k: request.args[k] for k in fields }
    player_list = db.players(spec=spec, fields=PLAYER_FIELDS_DICT)
    return bson.json_util.dumps(player_list)

@app.route('/api/player', methods=[ 'GET', 'POST' ])
@enforce_present(get_args=['uniqname'], post_args=['uniqname'])
def json_player(args=None):
    if request.method == 'GET':
        uniqname = request.args['uniqname']
        player = db.player_if_exists(uniqname, fields=PLAYER_FIELDS)
        return bson.json_util.dumps(player)

    elif request.method == 'POST':
        update_keys = set(PLAYER_FIELDS) & set(request.form.keys())
        new_doc = { k: request.form[k] for k in update_keys }
        db.update(uniqname, new_doc)
        player = db.player_if_exists(uniqname, fields=PLAYER_FIELDS)
        return json.dumps(player)
