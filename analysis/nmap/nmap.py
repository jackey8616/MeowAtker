from __future__ import unicode_literals, print_function 
import os

from utils.Message import Message
from utils.println import printText
from parse import parse
from upload import upload
from upload import serverProcess as uServerProcess

class Nmap(object):
    
    def __init__(self, analysis):
        self.analysis = analysis
        self.redis = self.analysis.redis
        self.ftp = self.analysis.ftp
        self.printField = self.analysis.printField

    def process(self, select, user_input=''):
        if 'Status' in select or user_input.startswith('status'):
            pass
        elif 'Parse' in select or user_input.startswith('parse'):
            return 'Nmap ' + parse(self.analysis, self.redis, self.printField, user_input.replace('parse ', ''))
        elif 'Upload' in select or user_input.startswith('upload'):
            return 'Nmap ' + upload(self.ftp, self.redis, self.printField, user_input.replace('upload ', ''))
        elif user_input.startswith('back'):
            printText('Analysis > ')
            return ''
        elif user_input.startswith('help'):
            printText('status      - Status all nmap records\nparse     - Parse a nmap XML file.\nupload      - Upload a nmap XML file for analysis.\nAnalysis Nmap > ')
        else:
            printText('Analysis Nmap > ')
            return 'Nmap '

    def serverProcess(self, msg):
        nextRoute = msg.nextRoute()
        if nextRoute == 'Parse':
            pass
        elif nextRoute == 'Upload':
            uServerProcess(self.analysis, msg)
