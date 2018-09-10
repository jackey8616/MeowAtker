import traceback, threading, copy
from threading import Event

from prompt_toolkit.document import Document
from prompt_toolkit.widgets import TextArea

from Message import Message
from println import printText

class Dashboard(threading.Thread):

    def __init__(self, redis, exploit, defense, analysis, printField, loopDelay=1, debug=False):
        super(Dashboard, self).__init__()
        self.stopped = Event()
        self.loopDelay = loopDelay

        self.debug = debug
        self.exploit = exploit
        self.defense = defense
        self.analysis = analysis
        self.redis = redis
        self.printField = printField

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            if self.debug:
                printText('heart-beat')
            if not self.redis.message.empty():
                message = self.redis.message.get(timeout=1)
                printText(message)
                self.processMessage(message)

    def stop(self):
        self.stopped.set()

    def process(self, select, user_input=''):
        if 'help' in select or user_input.startswith('help'):
            printText('init        - Init service\nstop        - Stop service\nexit        - Stop and clode service\n\nexploit     - Enter exploit interface\ndefense     - Enter defense interface\nanalysis    - Enter analysis interface\n')
        else:
            printText('Unknown command, maybe "help" or ctrl+o can let you know somthing.')
            

    def processMessage(self, msg):
        try:
            message = Message.fromJson(msg)
            nextRoute = message.nextRoute()
            if nextRoute == 'Analysis':
                self.analysis.serverProcess(message)
        except:
            if self.debug:
                printText(traceback.format_exc(), end='')
