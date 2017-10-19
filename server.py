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
  '''
  Register new client on server.
  register(username, ip, port) -> boolean
  '''
  try:
    #Checks if username is already on userlist return false.
    for u in userlist:
      if u['username'] == username:
        return False

    #Adds username to userlist
    u = User(username, ip, port)
    userlist.append(u.__dict__)

  #If port or ip are invalid, throw exception and return false.
  except ValueError:
    return False
  #If it's added sucessfully, return true.
  else:
    print username + " registered sucessfully"
    return True

def list_users():
  '''
  Lists all usernames registered on server.
  list_users() -> userlist
  '''
  return userlist

def main():
  HOST = "localhost"
  PORT = 8000
  server = SimpleXMLRPCServer((HOST, PORT))
  print "Host " + HOST + " listening on port " + str(PORT) +"..."

  server.register_function(register)
  server.register_function(list_users, 'list')
  server.register_introspection_functions()
  server.serve_forever()


if __name__ == "__main__":
  main()