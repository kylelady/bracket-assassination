import conn

mongo = conn.get_dbconnection()

class User(object):

    admins = [ 'kylelady', 'davadria' ]

    def __init__(self, uniqname, full_name=None):
        self._uniqname = uniqname
        self.full_name = full_name

    @property
    def uniqname(self):
        return self._uniqname

    @property
    def is_admin(self):
        return True
        #return self.uniqname in User.admins

    @classmethod
    def from_dict(cls, db_user):
        uniqname = db_user['uniqname']
        full_name = db_user.get('full_name', None)
        return User(uniqname,
            full_name=full_name
            )

    @classmethod
    def from_uniqname(cls):
        try:
            db_user = mongo.users.find_one(spec={'uniqname': uniqname})
            if db_user:
                return from_dict(db_user)
        except conn.MongoError:
            raise conn.DatabaseError
        return None



    