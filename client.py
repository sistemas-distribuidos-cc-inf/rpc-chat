import xmlrpclib

proxy = xmlrpclib.ServerProxy("http://localhost:8000/")

proxy.register("joao", "127.0.0.1", 1234)
u = proxy.list_user()

print u