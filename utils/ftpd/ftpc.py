import os
from ftplib import FTP_TLS

class ftpc(object):

    def __init__(self, ip, port):
        assert ip != None
        assert port != None
        self.ip = ip
        self.port = port

    def start(self):
        self.ftpc = FTP_TLS(timeout=5.0)
        self.ftpc.connect(self.ip, int(self.port))
        self.ftpc.login('asuka', 'meowmeowmeow')

    def stop(self):
        self.ftpc.quit()

    def upload(self, path):
        try:
            with open(path, 'rb') as f:
                self.start()
                fileName = os.path.split(path)[-1]
                self.ftpc.storbinary('STOR %s' % fileName, f, 8192)
                self.stop()
        except Exception as e:
            print(e)

