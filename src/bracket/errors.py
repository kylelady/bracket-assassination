import const

class AssassinationException(Exception):
    
    def __init__(status=const.STATUS_ERROR, msg=const.DEFAULT_ERROR_MSG, 
                 *args, **kwargs):
        super(AssassinationException).__init__(self, *args, **kwargs)
        self.status = status
        self.msg = msg

class InvalidRequest(AssassinationException):
    
    def __init__(msg='Invalid Request', *args, **kwargs):
        super(InvalidRequest).__init__(self, status=const.STATUS_CLIENT_ERROR,
                                       msg=msg, *args, **kwargs)

class MissingParameter(InvalidRequest):

    def __init__(param_name, *args, **kwargs):
        msg = 'Missing required parameter: %s' % param_name
        super(MissingParameter).__init__(
            self, 
            status=const.STATUS_CLIENT_ERROR,
            msg=msg,
            *args,
            **kwargs
            )


class AuthenticationError(AssassinationException):
    
    def __init__(msg='Access Denied', *args, **kwargs):
        super(AuthenticationError).__init__(
            self, 
            status=const.STATUS_CLIENT_ERROR,
            msg=msg, 
            *args, 
            **kwargs
            )