import sys, threading, traceback, redis, Queue
from threading import Event

from println import printText 

class RedisManager(threading.Thread):

    def __init__(self, ip, port, printField, loopDelay=300, maxsize=100, debug=False):
        super(RedisManager, self).__init__()
        assert ip != None
        assert port != None

        self.loopDelay = loopDelay
        self.stopped = Event()
        self.printField = printField
        self.debug = debug
        self.ip = ip
        self.port = port
        self.rd = None
        self.ps = None

        self.message = Queue.Queue(maxsize=maxsize)

    def connect(self, user):
        try:
            assert user != None

            # Constructing pools and redis server connection.
            self.rd = redis.Redis(host=self.ip, port=self.port)
            # Set to Subscribe / Publish mode.
            self.ps = self.rd.pubsub()
            self.ps.subscribe(['Dashboard', 'Exploit', 'Analysis', 'Defense'])
            self.rd.publish('Dashboard', 'User: %s connected, Role: %s' % (user.getUserName(), user.getRole()))
            printText(self.printField, 'Redis channels inited')
        except Exception as e:
            if (self.debug):
                traceback.print_exc()
            sys.exit(1)

    def start(self):
        super(RedisManager, self).start()
        printText(self.printField, 'Redis inited.')

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            for each in self.ps.listen():
                if each['type'] == 'message':
                    self.message.put(each['data'])
                    printText(self.printField, each['data'])

    def stop(self):
        self.stopped.set()
        printText(self.printField, 'Redis exit signal setted.')

    def isExit(self):
        return self.stopped.isSet()

