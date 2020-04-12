#-*- coding:utf-8 -*-
#-*- encoding : UTF-8 -*-
from __future__ import absolute_import, division, print_function

from twisted.web import server, resource
from twisted.internet import reactor, defer
from importlib import import_module
import json
import os

def convertJsonToDict(data):
	return json.loads(data)

def convertDictToJson(data):
	return json.dumps(data)

class DummyServer(resource.Resource):
	isLeaf = True
	def __init__(self, uriDict): 
		self.uriDict = uriDict

	def render_POST(self, request):
		print("Received request for {0}".format(request.uri))
		uri = request.uri.replace('/','')
		contextType = request.getHeader('Context-Type')
		ret = {'data': None, 'code':200}
		if contextType != 'application/json':
			ret['code'] = 400    
		else:
			ret['data'], ret['code'] = self._uriContext(uri)
        
		request.setHeader('Content-Type', 'application/json')
		request.setResponseCode(ret['code'])
		return convertDictToJson(ret)

	def _uriContext(self, uri):
		if uri in self.uriDict:
			mod = uriDict[uri].split('.')

    		# uriImport : 임포트 할 모듈명
			# uriFunc : 임포트 할 함수명
			uriImport = '.'.join(mod[0:-1])
			uriFunc = mod[-1]

			# m : 임포트된 모듈 핸들러
			# func : 가져온 함수 핸들러
			m = import_module(uriImport)
			return getattr(m, uriFunc)(), 200
		else:
			print("Immediate answering request for '/'")
			return "Not Found", 404


def getUriMapping():
	import xml.etree.ElementTree as ET

	xmlTree = ET.parse(os.path.join(os.getcwd(), 'conf', 'url-mapping.xml'))
	uriAttr = xmlTree.getroot().findall('uri')
	func = lambda uri:map(uri.get, [k for k in uri.keys() if k=='name' or k =='func'])
	return {data[0]:data[1] for data in map(func, uriAttr) if data != []}

if __name__ == '__main__':
	uriDict = getUriMapping()
	print(uriDict)
	s = server.Site(DummyServer(uriDict))
	reactor.listenTCP(9990, s)
	reactor.run()
