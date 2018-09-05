import os
from subprocess import Popen, PIPE

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

        #if self.isServer():
            #self.ftps = ftps('0.0.0.0', self.port, self.path)
        self.ftpc = ftpc(self.ip, self.port)
    
    def isServer(self):
        return self.user.getRole() == 'None'

    def isClient(self):
        return not self.isServer()

    def upload(self, path):
        print('Start uploading file from: %s' % path)
        self.ftpc.upload(path)

    def start(self):
        if self.isServer():
            #self.ftps.start()
            self.ftps = Popen(['python', './utils/ftpd/ftps.py', '--ip', '0.0.0.0', '--path', self.path], stdout=PIPE)
            print('FTP Server inited.')

    def stop(self):
        if self.isServer():
            #self.ftps.stop()
            self.ftps.kill()
            print('FTP Server stopped.')

if __name__ == '__main__':
    ftpHandler = FTPHandler('127.0.0.1', 21, os.getcwd())
