import admin

import cyclone.web

url_handlers = [
	(r'/api/players/', admin.PlayerHandler),
	(r'/api/players/([A-Za-z]+)', admin.SinglePlayerHandler),
	(r'/api/players/([A-Za-z]+)/delete/', admin.SinglePlayerHandler),
	(r'/admin/', admin.AdminHandler),
	(r'/static/(.*)', cyclone.web.StaticFileHandler, {'path': 'static'}),
]