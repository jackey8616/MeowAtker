import json

class Message(object):

    def __init__(self, channel, route, content):
        self.channel = channel
        self.route = route
        self.content = content

    def toJson(self):
        return json.dumps({ 'channel': self.channel, 'route': self.route, 'content': self.content })

    def nextRoute(self):
        nextRoute = self.route.split(' ')[0]
        self.route = self.route.replace('%s ' % nextRoute, '')
        return nextRoute

    @staticmethod
    def fromJson(msg):
        jsonObj = json.loads(msg)
        return Message(jsonObj['channel'], jsonObj['route'], jsonObj['content'])

