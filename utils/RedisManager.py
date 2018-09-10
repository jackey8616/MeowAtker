import sys, threading, traceback, redis, Queue
from threading import Event

from println import printText 

class RedisManager(threading.Thread):

    def __init__(self, ip, port, printField, user, loopDelay=1, maxsize=100, debug=False):
        super(RedisManager, self).__init__()
        assert ip != None
        assert port != None
        assert user != None

        self.loopDelay = loopDelay
        self.stopped = Event()

        self.debug = debug
        self.printField = printField
        self.user = user
        self.ip = ip
        self.port = port
        self.rd = None
        self.ps = None

        self.message = Queue.Queue(maxsize=maxsize)

    def connect(self):
        try:
            # redis server connection.
            self.rd = redis.Redis(host=self.ip, port=self.port)
            # Set to Subscribe / Publish mode.
            self.ps = self.rd.pubsub()
            self.ps.subscribe(['Dashboard', 'Exploit', 'Analysis', 'Defense'])
            self.rd.publish('Dashboard', 'User: %s connected, Role: %s' % (self.user.getUserName(), self.user.getRole()))
            printText('Redis channels inited')
        except Exception as e:
            if (self.debug):
                traceback.print_exc()
            sys.exit(1)

    def start(self):
        super(RedisManager, self).start()
        self.connect()
        printText('Redis inited.')

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            message = self.ps.get_message()
            if message and message['type'] == 'message':
                self.message.put(message['data'])
        self.ps.close()

    def sendMessage(self, message):
        self.rd.publish(message.channel, message.toJson())

    def stop(self):
        self.stopped.set()
        printText('Redis exit signal setted.')

    def isExit(self):
        return self.stopped.isSet()

