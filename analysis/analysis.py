from __future__ import unicode_literals, print_function 

from nmap import Nmap
from openvas import Openvas

from utils.println import printText

class Analysis(object):

    def __init__(self, redis, session, ftp, printField):
        self.redis = redis
        self.ftp = ftp
        self.printField = printField

        self.nmap = Nmap(self)
        self.openvas = Openvas(self)

    def process(self, select, user_input=''):
        if 'Nmap' in select or user_input.startswith('nmap'):
            return 'Analysis ' + self.nmap.process(select, user_input.replace('nmap ', ''))
        elif 'Openvas' in select or user_input.startswith('openvas'):
            return 'Analysis ' + self.openvas.process(select, user_input.replace('openvas ', ''))
        elif user_input.startswith('back'):
            printText(self.printField, '> ')
            return ''
        elif user_input.startswith('help'):
            printText(self.printField, 'nmap        - Enter nmap interface\nopenvas     - Enter openvas interface\nAnalysis > ')
            return 'Analysis'
        else:
            printText(self.printField, 'Analysis > ')
            return 'Analysis'

