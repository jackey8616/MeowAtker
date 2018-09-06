import threading, copy
from threading import Event

from prompt_toolkit.document import Document
from prompt_toolkit.widgets import TextArea

from println import printText

class Dashboard(threading.Thread):

    def __init__(self, redis, printField, loopDelay=1):
        super(Dashboard, self).__init__()
        self.stopped = Event()
        self.loopDelay = loopDelay
        self.redis = redis
        self.printField = printField

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            printText(self.printField, 'jb')
            if not self.redis.message.empty():
                printText(self.printField, self.redis.message.get())

    def stop(self):
        self.stopped.set()

    

