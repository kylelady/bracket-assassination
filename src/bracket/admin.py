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


@require_admin
@app.route('/admin', methods=['GET'])
def admin():
    return display_admin_panel()

