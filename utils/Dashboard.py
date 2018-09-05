import threading, copy
from threading import Event

class Dashboard(threading.Thread):

    def __init__(self, redis, loopDelay=10):
        super(Dashboard, self).__init__()
        self.stopped = Event()
        self.loopDelay = loopDelay
        self.redis = redis

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            print('hb')
            if not self.redis.message.empty():
                print(self.redis.message.get())

    def stop(self):
        self.stopped.set()

    

