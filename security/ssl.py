#from twisted.internet import ssl, reactor, endpoints
from twisted.internet import endpoints
def createSSL(reactor):
    return endpoints.serverFromString(
		reactor, 
		'ssl:9990:interface=0.0.0.0:certKey=conf/keys/server.crt:privateKey=conf/keys/server.pem'
	)
