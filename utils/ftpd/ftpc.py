from ftplib import FTP

class ftpc(object):

    def __init__(self, ip, port):
        assert ip != None
        assert port != None

        self.ftpc = FTP('')

    def start(self):
        self.ftpc.connect(self.ip ,self.port)
        self.ftpc.login('asuka', 'meowmeowmeow')

    def exit(self):
        self.ftpc.quit()

    def upload(self, path):
        with open(path, 'rb') as f:
            fileName = os.path.slit(path)[-1]
            self.ftpc.storbinary('STOR %s' % fileName, f, 8192)

