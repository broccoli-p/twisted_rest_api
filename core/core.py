from twisted.web import server, resource

from importlib import import_module
from urllib2 import unquote
from ast import literal_eval
import os, sys
from common.database.oracle_connect import Connection
from common.common_func import *
from error.exception import *

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

class Server(resource.Resource):
    isLeaf = True
    def __init__(self, uriDict = None): 
        if uriDict is None:
            self.uriDict = self._getUriMapping()
        else :
            self.uriDict = uriDict
        try:
            Connection()
        except DatabaseError as err:
            lineno = sys.exc_info()[2].tb_lineno			
            raise Exception(getErrorStr(sys._getframe(), err, lineno))

    def render(self, request):
        ret = self._setReturnData(request)
        request.setHeader('Content-Type', 'application/json')
        request.setResponseCode(ret['code'])
        return convertDictToJson(ret)

    def _setReturnData(self, request):
        # Get default information
        uri = '.'.join(request.uri.split('/')[1:])# sync.person
        method = request.method
        contextType = request.getHeader('Context-Type')

        # context type check - only json
        ret = {'data': None, 'code':400}
        if contextType != 'application/json':
            ret['code'] = 400
            ret['data'] = "Parameter requirements violated(Context type is application/json)"
            return ret
        try:
            #a = dictCodecsUnicode(literal_eval(unquote(uriString[1])))
            a = dictCodecsUnicode(literal_eval(request.content.read()))
            print a
        except SyntaxError as err:
            ret['data'] = "1. Parameter requirements violated(Parameter is not of type json)"
            return ret
        try:
            ret['data'], ret['code'] = self._uriContext(uri, method, a)
        except TypeError as err:
            ret['data'] = "Parameter requirements violated(%s)" %err
        except ValueError as err:
            ret['data'] = "Parameter requirements violated(Parameter is not of type json)"
        except Exception as err:
            ret['data'] = "SERVER_ERROR:%s" %err
            ret['code'] = 500
        try:
            return convertUnicodeToStr(ret)
        except Exception as err:
            ret['data'] = str(err)
            ret['code'] = 400
            return ret
    def _uriContext(self, uri, method, data):
        print uri 
        if uri in self.uriDict:
            try:
                func = self.uriDict[uri][method]
            except KeyError as err:
                return "Feature not implemented", 400

            m = import_module(uri)
            return getattr(m, func)(data), 200
			
        else:
            return "Not Found", 404

    def _getUriMapping(self):
        import xml.etree.ElementTree as ET
        xmlTree = ET.parse(os.path.join(os.path.dirname(
                os.path.abspath(os.path.dirname(__file__))),
                'conf', 'url-mapping.xml'))
        uriAttr = xmlTree.getroot().findall('uri')
        rootPack = xmlTree.getroot().find('root-package').attrib['value']
        return {'.'.join([rootPack, uri.attrib['target']]):{x.attrib['type']
                    .upper():x.attrib['func'] 
                        for x in uri} for uri in uriAttr}

    def __del__(self):
        Connection.disconnection()
