from . import app

from . import errors, db

import json
import bson.json_util

from flask.views import MethodView

class MatchApi(MethodView):

    def get(self, match_id):
        spec = dict()
        if match_id is not None:
            spec['_id'] = match_id
        result = db.matches(spec)
        return bson.json_util.dumps(result)

    def post(self, favorite, underdog):
        pass

match_view = MatchApi.as_view('match_api')
app.add_url_rule('/matches/', defaults={'match_id': None},
                 view_func=match_view, methods=['GET'])