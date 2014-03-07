import cyclone.web
import json

import const
import errors
from db import users

def authenticated(f):
    def wrapper(self, *args, **kwargs):
        self.user = users.FromCosign(self.request)
        f(self, *args, **kwargs)
    return wrapper

def require_admin(f):
    def wrapper(self, *args, **kwargs):
        if not self.user.is_admin:
            raise errors.AuthenticationError
        f(*args, **kwargs)
    return wrapper

class AssassinationHandler(cyclone.web.RequestHandler):

    def get(self, *args, **kwargs):
        try:
            self.handle_get(*args, **kwargs)
        except errors.AssassinationException as e:
            self._error(e)

    def post(self, *args, **kwargs):
        try:
            self.handle_post(*args, **kwargs)
        except errors.AssassinationException as e:
            self._error(e)

    def _error(self, error):
        if error.status == const.STATUS_CLIENT_ERROR:
            self.send_error(300, error.msg)
        else:
            self.send_error(500, error.msg)

class ApiHandler(AssassinationHandler):

    def make_response(self, body=None, status=const.STATUS_OK, msg=None):
        obj = {
            'status': status,
        }
        if body is not None:
            obj['body'] = body
        if status != const.STATUS_OK:
            if msg is not None:
                obj['msg'] = msg
            else:
                obj['msg'] = 'Unknown Error'
        self.write(obj)

    def _error(self, error):
        res = self.make_response('', status=error.status, msg=error.msg)


