from src.bracket import routes

import cyclone.web
import sys

from twisted.internet import reactor
from twisted.python import log

import os

if __name__ == "__main__":

    settings = {
        'template_path': 'html',
        'debug': True,
    }

    application = cyclone.web.Application(
        routes.url_handlers,
        **settings
    )
    log.startLogging(sys.stdout)
    reactor.listenTCP(8888, application)
    reactor.run()