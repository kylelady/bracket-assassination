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
    #    if not self.user.is_admin:
    #        raise errors.AuthenticationError
        f(*args, **kwargs)
    return wrapper

