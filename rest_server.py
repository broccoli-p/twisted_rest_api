#-*- coding:utf-8 -*-
#-*- encoding : UTF-8 -*-
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
		# uriImport : 임포트 할 모듈명
		# uriFunc : 임포트 할 함수명
		self.uriName = uriDict[0]
		self.uriImport = uriDict[1].split(".")[0] + "."
		self.uriImport = self.uriImport + uriDict[1].split(".")[1]
		self.uriFunc = uriDict[1].split(".")[2]

		# m : 임포트된 모듈 핸들러
		# func : 가져온 함수 핸들러
		m = import_module(self.uriImport)
		self.func = getattr(m, self.uriFunc)

	def render_POST(self, request):
		print("Received request for {0}".format(request.uri))
		uri = request.uri.replace('/','')
		context_type = request.getHeader('Context-Type')
		ret = {'data': None, 'code':200}
		if context_type != 'application/json':
			ret['code'] = 400    
		else:
			ret['data'], ret['code'] = self._uriContext(uri)
        
		request.setHeader('Content-Type', 'application/json"')
		request.setResponseCode(ret['code'])
		return convertDictToJson(ret)

	def _uriContext(self, uri):
		if uri in self.uriName:
			# ret : 함수 결과값 불러오기
			ret = self.func()
			return {'err':'True', 'data':ret}, 200
		else:
			print("Immediate answering request for '/'")
			return "Not Found", 404


def getUriMapping():
	import xml.etree.ElementTree as ET

	xml_tree = ET.parse(os.path.join(os.getcwd(), 'conf', 'url-mapping.xml'))
	uriDict = xml_tree.getroot().findall('uri')
	func = lambda uri:map(uri.get, [k for k in uri.keys() if k=='name' or k =='func'])
	for x in map(func, uriDict):
		data = x
	return data

if __name__ == '__main__':
	uriDict = getUriMapping()
	print(uriDict)
	s = server.Site(DummyServer(uriDict))
	reactor.listenTCP(9990, s)
	reactor.run()
