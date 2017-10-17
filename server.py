import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

userlist = []

class User:
	"""User class"""
	def __init__(self, username, ip, port):
		self.username = username
		self.ip = ip
		self.port = port


def register(username, ip, port):
	try:
		for u in userlist:
			if u['username'] == username:
				return False

		u = User(username, ip, port)
		userlist.append(u.__dict__)

	except ValueError:
		return False		
	else:
		return True

def list_user(username = ""):
	if username != "":
		for u in userlist:
			if u['username'] == username:
				return u
	else:
		return userlist


def main():
	HOST = "localhost"
	PORT = 8000
	server = SimpleXMLRPCServer((HOST, PORT))
	print "Listening on port " + str(PORT) +"..." 

	server.register_function(register)
	server.register_function(list_user)

	server.serve_forever()


if __name__ == "__main__":
	main()