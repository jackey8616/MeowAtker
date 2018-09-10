import os

import xml.etree.ElementTree as ET
from utils.Target.Target import Target
from utils.Message import Message
from utils.println import printText

def upload(ftp, redis, printField, path):
    printText('Analysis Nmap Upload > ', outputField=printField)
    if path == 'upload':
        pass
    else:
        if(os.path.isfile(path)):
            fileName = os.path.split(path)[-1]
            printText('Uploading: %s' % path, outputField=printField)
            ftp.upload(path)
            printText('Uploaded: %s' % fileName, outputField=printField)
            redis.sendMessage(Message('Analysis', 'Analysis Nmap Upload', fileName))
        else:
            printText('This is not a valid file.', outputField=printField)
    return 'Upload'

def serverProcess(analysis, msg):
    fileName = msg.content
    #fileName = msg
    Target.newByXMLFile(fileName)
    #tree = ET.parse(fileName)
    printText('Analysis nmap xml down', outputField=analysis.printField)

if __name__ == '__main__':
    serverProcess(None, './140.125.207.1_100.xml')
