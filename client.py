import xmlrpclib
import socket
import threading
import thread

# TODO: pedir para o usuario digitar a porta
HOST = "localhost"
PORT = 1234

class ServerThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.conn = None
		self.addr = None

	def run(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((HOST, PORT))
		s.listen(1)
		
		self.conn, self.addr = s.accept()
		while True:
			msg = self.conn.recv(1024)
			if msg == "quit":
				break
			print msg
		self.conn.close()


class ClientThread(threading.Thread):
	def __init__(self, host, port):
		threading.Thread.__init__(self)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((host, port))

	def run(self):
		while True:
			msg = raw_input()
			if msg == 'quit':
				self.sock.send("quit")
				print "bye"
				break
			else:
				self.sock.sendall(msg)

		self.sock.close()


def main():
	proxy = xmlrpclib.ServerProxy("http://localhost:8000/")

	proxy.register("joao", "127.0.0.1", 1234)
	u = proxy.list_users()

	st = ServerThread()
	st.start()

	ct = ClientThread(HOST, PORT)
	ct.start()


if __name__ == "__main__":
	main()