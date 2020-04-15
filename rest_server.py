#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function

from twisted.web import server, resource
from twisted.internet import reactor, defer, ssl, endpoints
from importlib import import_module
from urllib2 import unquote
from ast import literal_eval


from common import simpleJson

import os, sys, json

class DummyServer(resource.Resource):
	isLeaf = True
	def __init__(self, uriDict): 
		self.uriDict = uriDict
	
	def render(self, request):
		print("Received request for {0}".format(request.uri))

		ret = self._setReturnData(request)
		request.setHeader('Content-Type', 'application/json')
		request.setResponseCode(ret['code'])
		return simpleJson.convertDictToJson(ret)

	def _setReturnData(self, request):
		# Get default information
		uriString = request.uri.split('?')
		uri = '.'.join(uriString[0].split('/')[1:])
		method = request.method
		contextType = request.getHeader('Context-Type')

		# context type check - only json
		ret = {'data': None, 'code':200}
		if contextType != 'application/json':
			ret['code'] = 400   
			ret['data'] = "Parameter requirements violated(Context type is application/json)"
			return ret
	
		try:
			ret['data'], ret['code'] = self._uriContext(uri, method, literal_eval(unquote(uriString[1])))
		except TypeError as err:
			ret['code'] = 400
			ret['data'] = "Parameter requirements violated(%s)" %err
		except ValueError as err:
			ret['code'] = 400
			ret['data'] = "Parameter requirements violated(Parameter is not of type json)"
		except Exception as err:
			ret['code'] = 400
			ret['data'] = "%s" %err

		return ret

	def _uriContext(self, uri, method, data):
		
		if uri in self.uriDict:
			try:
				func = uriDict[uri][method]
			except KeyError as err:
				return "Feature not implemented", 400
			# m : 임포트된 모듈 핸들러
			# func : 가져온 함수 핸들러
			m = import_module(uri)
			return getattr(m, func)(data), 200
		else:
			return "Not Found", 404


def getUriMapping():
	import xml.etree.ElementTree as ET
	xmlTree = ET.parse(os.path.join(os.path.dirname(
				os.path.abspath(__file__)), 'conf', 'url-mapping.xml'))
	uriAttr = xmlTree.getroot().findall('uri')
	return {uri.attrib['target']:{x.attrib['type'].upper():x.attrib['func'] for x in uri} for uri in uriAttr}

if __name__ == '__main__':

	uriDict = getUriMapping()
	print(uriDict)
	s = server.Site(DummyServer(uriDict))

	httpsServer = endpoints.serverFromString(
		reactor, 
		'ssl:9990:interface=0.0.0.0:certKey=conf/keys/server.crt:privateKey=conf/keys/server.pem'
	)
	httpsServer.listen(s)
	reactor.run()
