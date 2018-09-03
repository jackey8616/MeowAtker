from __future__ import unicode_literals, print_function 

from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout

from nmap import Nmap
from openvas import Openvas

class Analysis(object):

    def __init__(self, ftp):
        self.ftp = ftp
        self.nmap = Nmap(self, ftp)
        self.openvas = Openvas(self, ftp)

    def process(self):
        with patch_stdout():
            text = '''nmap        -   nmap detail
openvas     -   openvas detail
back        -   back to menu
Analysis > '''
            user_input = prompt(text)
            if user_input == 'nmap':
                self.nmap.process()
            elif user_input == 'openvas':
                self.openvas.process()
            elif user_input == 'back':
                pass
