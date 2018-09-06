from __future__ import unicode_literals, print_function 
import os

from utils.println import printText

class Nmap(object):
    
    def __init__(self, analysis):
        self.analysis = analysis
        self.ftp = self.analysis.ftp
        self.printField = self.analysis.printField

    def process(self, select, user_input=''):
        if 'Status' in select or user_input.startswith('status'):
            pass
        elif 'Upload' in select or user_input.startswith('upload'):
            return 'Nmap ' + self.upload(user_input.replace('upload ', ''))
        elif user_input.startswith('back'):
            printText(self.printField, 'Analysis > ')
            return ''
        elif user_input.startswith('help'):
            printText(self.printField,'status      - Status all nmap records\nupload      - Upload a nmap XML file for analysis.\nAnalysis Nmap > ')
        else:
            printText(self.printField, 'Analysis Nmap > ')
            return 'Nmap '

    def upload(self, path):
        printText(self.printField, 'Analysis Nmap Upload > ')
        if path == 'upload':
            pass
        else:
            if(os.path.isfile(path)):
                self.ftp.upload(path)
            else:
                printText(self.printField, 'This is not a valid file.')
        return 'Upload'
