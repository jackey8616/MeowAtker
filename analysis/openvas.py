from __future__ import unicode_literals, print_function 

from prompt_toolkit.patch_stdout import patch_stdout

class Openvas(object):

    def __init__(self, analysis, ftp):
        self.analysis = analysis
        self.session = self.analysis.session
        self.ftp = ftp

    def process(self, user_input=''):
        with patch_stdout():
            if user_input == '' or user_input == 'openvas':
                text = '''status      -   print all openvas information.
add         -   add a openvas information.
back        -   back to analysis menu.
Analysis.openvas > '''
                user_input = self.session.prompt(text)
        if user_input == 'back':
            self.analysis.process()
