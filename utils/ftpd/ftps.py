import os, threading

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import TLS_FTPHandler
from pyftpdlib.servers import FTPServer, ThreadedFTPServer

class ftps(threading.Thread):

    def __init__(self, ip, port, path):
        super(ftps, self).__init__()
        assert ip != None
        assert port != None
        assert path != None

        if not os.path.exists(path):
            os.makedirs(path)

        authorizer = DummyAuthorizer()
        authorizer.add_user('asuka', 'meowmeowmeow', path, perm='elradfmwMT')

        handler = TLS_FTPHandler
        handler.certfile = os.path.abspath(os.path.join(os.path.dirname(__file__), 'keycert.pem'))
        handler.authorizer = authorizer

        self.server = FTPServer((ip, port), handler)

    def run(self):
        self.server.serve_forever(timeout=1.0, blocking=False)

    def smoothExit(self):
        self.server.close()

    def exit(self):
        self.server.close_all()

    def checkPemFile(self, cePath):
        key = RSA.exportKey()
        pv_key_string = key.exportKey()
        with open('private.pem', 'w') as prv_file:
            prv_file.write("{}".format(pv_key_string.decode()))

        pb_key_string = key.publicKey().exportKey()
        with open('public.pem', 'w') as pub_file:
            pub_file.write("{}".format(pb_key_string.decode()))

if __name__ == '__main__':
    server = ftps('127.0.0.1', 21, os.getcwd())
    server.start()
    print(server)
    server.exit()
