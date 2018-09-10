import os, threading
from threading import Event
from subprocess import Popen, PIPE

from ftps import ftps
from ftpc import ftpc

from utils.println import printText

class FTPHandler(threading.Thread):

    def __init__(self, ip, port, path, user, printField, loopDelay=1):
        super(FTPHandler, self).__init__()
        assert ip != None
        assert port != None
        assert path != None
        assert user != None

        self.stopped = Event()
        self.loopDelay = loopDelay
        self.printField = printField
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
        printText('Start uploading file from: %s' % path)
        self.ftpc.upload(path)

    def start(self):
        if self.isServer():
            #self.ftps.start()
            self.ftps = Popen(['python', './utils/ftpd/ftps.py', '--ip', '0.0.0.0', '--path', self.path], stderr=PIPE)
            printText('FTP Server inited.')
            super(FTPHandler, self).start()

    def run(self):
        if self.isServer():
            while not self.stopped.wait(self.loopDelay):
                line = self.ftps.stderr.readline()
                if line != '':
                    printText(str(line), end='')

    def stop(self):
        if self.isServer():
            #self.ftps.stop()
            self.stopped.set()
            self.ftps.kill()
            printText('FTP Server stopped.')

if __name__ == '__main__':
    ftpHandler = FTPHandler('127.0.0.1', 21, os.getcwd())
