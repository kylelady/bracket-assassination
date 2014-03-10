import cyclone.web
import json

import const
import errors

import bson.json_util


class RequestHandler(cyclone.web.RequestHandler):

	def write_mongo_obj(self, mongo_obj):
		res = bson.json_util.dumps(mongo_obj)
		print res
		self.set_header('Content-Type', 'application/json')
		self.write(res)

