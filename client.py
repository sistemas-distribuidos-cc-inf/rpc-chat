import xmlrpclib
import socket
import threading


class ServerThread(threading.Thread):
  def __init__(self, host, port):
    threading.Thread.__init__(self)
    self.host = host
    self.port = port
    self.conn = None
    self.addr = None

  def run(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((self.host, self.port))
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
      msg = raw_input("=>")
      if msg == 'quit':
        self.sock.send("quit")
        print "bye"
        break
      else:
        self.sock.sendall(msg)

    self.sock.close()


def main():
  proxy = xmlrpclib.ServerProxy("http://localhost:8000/")

  username = raw_input("username: ")
  ip = raw_input("ip: ")
  port = int(raw_input("port: "))

  st = ServerThread(ip, port)
  st.start()

  proxy.register(username, ip, port)

  while True:
    msg = raw_input()

    if msg == 'list':
      user_list = proxy.list()
      print "Available users:"
      for u in user_list:
        print u
    else:
      action, person = msg.split(" ", 1)
      user_list = proxy.list()
      if action == 'talk':
        for u in user_list:
          if person == u['username']:
            ct = ClientThread(u['ip'], int(u['port']))
            ct.start()


if __name__ == "__main__":
  main()