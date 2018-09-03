import os

from ftps import ftps
from ftpc import ftpc

class FTPHandler(object):

    def __init__(self, ip, port, path, user):
        assert ip != None
        assert port != None
        assert path != None
        assert user != None

        self.ip = ip
        self.port = port
        self.path = path
        self.user = user

        if self.isServer():
            self.ftps = ftps(self.ip, self.port, self.path)
        if self.isClient():
            self.ftpc = ftpc(self.ip, self.port)
    
    def isServer(self):
        return self.user.getRole() == 'None'

    def isClient(self):
        return not self.isServer()

    def start(self):
        if self.isServer():
            self.ftps = ftps(self.ip, self.port, self.path)
            self.ftps.start()
            print('FTP Server inited.')
        else:
            self.ftpc = ftpc(self.ip, self.port)
            print('FTP Client inited.')

    def exit(self):
        if self.isServer():
            self.ftps.exit()
            print('FTP Server stopped.')
        else:
            self.ftpc.exit()
            print('FTP Client stopped.')

if __name__ == '__main__':
    ftpHandler = FTPHandler('127.0.0.1', 21, os.getcwd())
