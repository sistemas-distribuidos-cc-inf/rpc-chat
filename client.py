import xmlrpclib
import socket
from threading import Thread

def serverThread(username, ip, port):
  udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  orig = (ip, port)
  udp.bind(orig)
  while True:
      msg, cliente = udp.recvfrom(1024)
      print msg
  udp.close()

def main():
  client = xmlrpclib.ServerProxy("http://localhost:8000/")

  username = raw_input("username: ")
  ip = raw_input("ip: ")
  port = int(raw_input("port: "))

  client.register(username, ip, port)

  ts = Thread(target=serverThread, args=(username, ip, port,))
  ts.start()

  while True:
    print "Type an action ('list' or 'talk'): "
    action = raw_input()

    if action == 'list':
      user_list = client.list()
      print "Available users:"
      for u in user_list:
        print u

    elif action == 'talk':
      print "Type username you want to talk to: "
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
      client.system.listMethods()


if __name__ == "__main__":
  main()