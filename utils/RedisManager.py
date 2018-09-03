import sys, threading, traceback, redis
from threading import Event

class RedisManager(threading.Thread):

    def __init__(self, ip, port, loopDelay=300, debug=False):
        super(RedisManager, self).__init__()
        assert ip != None
        assert port != None

        self.loopDelay = loopDelay
        self.stopped = Event()
        self.debug = debug
        self.ip = ip
        self.port = port
        self.rd = None
        self.ps = None

    def connect(self, user):
        try:
            assert user != None

            # Constructing pools and redis server connection.
            self.rd = redis.Redis(host=self.ip, port=self.port)
            # Set to Subscribe / Publish mode.
            self.ps = self.rd.pubsub()
            self.ps.subscribe(['Dashboard', 'Exploit', 'Analysis', 'Defense'])
            self.rd.publish('Dashboard', 'User: %s connected, Role: %s' % (user.getUserName(), user.getRole()))
            print('Redis inited')
        except Exception as e:
            if (self.debug):
                traceback.print_exc()
            sys.exit(1)

    def start(self):
        if self.stopped.isSet():
            self.stopped.clear()
            self.run()
        else:
            super(RedisManager, self).start()
        print('Redis inited.')

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            for each in self.ps.listen():
                if each['type'] == 'message':
                    print(each['data'])

    def stop(self):
        self.stopped.set()
        print('Redis exit signal setted.')

    def isExit(self):
        return self.stopped.isSet()

