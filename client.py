import xmlrpclib
import socket
from threading import Thread

class ServerThread(Thread):
	def __init__(self, username, ip, port = 0):
		Thread.__init__(self)
		self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.orig = (ip, port)

	def run(self):
		self.udp.bind(self.orig)
		while True:
			msg, cliente = self.udp.recvfrom(1024)
			print msg
		self.udp.close()


def main():
	client = xmlrpclib.ServerProxy("http://localhost:8000/")

	username = raw_input("Type your username: ")
  	# gets the ip of the host
 	ip = socket.gethostbyname(socket.gethostname())

	ts = ServerThread(username, ip)
	ts.setDaemon(True)
  	ts.start()

  	# gets the binded port
  	port = ts.udp.getsockname()[1]
  	
  	# register the user on the server
  	client.register(username, ip, port)

	while True:
  		print "Type an action ('list' or 'talk'): "
  		action = raw_input()

  		if action == 'list':
  			user_list = client.list()
  			print "Available users:"
  			for u in user_list:
  				print u

  		elif action == 'talk':
  			print "Type the username you want to talk to: "
  			person = raw_input()
  			user_list = client.list()
  			for u in user_list:
  				if person == u['username']:
  					udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  					dest = (u['ip'], u['port'])
  					print "Type your message: "
  					msg = raw_input()
  					msg = username + ": " + msg
  					udp.sendto (msg, dest)
  					udp.close()
  		else:
  			print "Invalid action\nAvailable actions: "
  			print client.system.listMethods()


if __name__ == "__main__":
	main()