from __future__ import unicode_literals, print_function 
import os

from prompt_toolkit.patch_stdout import patch_stdout

class Nmap(object):
    
    def __init__(self, analysis, ftp):
        self.analysis = analysis
        self.session = self.analysis.session
        self.ftp = ftp

    def process(self, user_input=''):
        with patch_stdout():
            if user_input == '' or user_input == 'nmap':
                text = '''status      -   print all nmap informations.
upload      -   upload a nmap file for analysis.
back        -   back to analysis menu.
Analysis.nmap > '''
                user_input = self.session.prompt(text)
            if user_input.startswith('upload'):
                self.upload(user_input.replace('upload ', ''))
            elif user_input == 'back':
                self.analysis.process()

    def upload(self, path=''):
        with patch_stdout():
            if path == '' or path == 'upload':
                path = self.session.prompt('Analysis.nmap.upload > ')
            if(os.path.isfile(path)):
                self.ftp.upload(path)
            else:
                print('This is not a valid file.')

