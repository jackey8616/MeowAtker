import os, click

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import TLS_FTPHandler
from pyftpdlib.servers import FTPServer, ThreadedFTPServer

@click.command()
@click.option('--ip', default='0.0.0.0', type=str)
@click.option('--port', default=21, type=int)
@click.option('--path', default=os.getcwd(), type=str)
def ftps(ip, port, path):

    if not os.path.exists(path):
        os.makedirs(path)

    users = [('asuka', 'meowmeowmeow')]
    authorizer = DummyAuthorizer()
    for (name, passwd) in users:
        if not os.path.exists('%s/%s' % (path, name)):
            os.makedirs('%s/%s' % (path, name))
        authorizer.add_user(name, passwd, '%s/%s' % (path, name), perm='elradfmwMT')
    
    handler = TLS_FTPHandler
    handler.certfile = os.path.abspath(os.path.join(os.path.dirname(__file__), 'keycert.pem'))
    handler.authorizer = authorizer
    
    server = ThreadedFTPServer((ip, port), handler)
    server.serve_forever()

if __name__ == '__main__':
    ftps()
