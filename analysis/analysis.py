from __future__ import unicode_literals, print_function 

from prompt_toolkit.patch_stdout import patch_stdout

from nmap import Nmap
from openvas import Openvas

class Analysis(object):

    def __init__(self, session, ftp):
        self.session = session
        self.ftp = ftp
        self.nmap = Nmap(self, ftp)
        self.openvas = Openvas(self, ftp)

    def process(self, user_input=''):
        with patch_stdout():
            if user_input == '' or user_input == 'analysis':
                text = '''nmap        -   nmap detail
openvas     -   openvas detail
back        -   back to menu
Analysis > '''
                user_input = self.session.prompt(text)
            if user_input.startswith('nmap'):
                self.nmap.process(user_input.replace('nmap ', ''))
            elif user_input.startswith('openvas'):
                self.openvas.process(user_input.replace('openvase ', ''))
            elif user_input == 'back':
                pass
