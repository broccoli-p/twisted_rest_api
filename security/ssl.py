from twisted.internet import ssl, reactor, endpoints

def createSSL():
    return endpoints.serverFromString(
		reactor, 
		'ssl:9990:interface=0.0.0.0:certKey=conf/keys/server.crt:privateKey=conf/keys/server.pem'
	)
