from __future__ import unicode_literals, print_function 

from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout

class Openvas(object):

    def __init__(self, analysis, ftp):
        self.analysis = analysis
        self.ftp = ftp

    def process(self):
        with patch_stdout():
            text = '''status      -   print all openvas information.
add         -   add a openvas information.
back        -   back to analysis menu.
Analysis.openvas > '''
        user_input = prompt(text)
        if user_input == 'back':
            self.analysis.process()
