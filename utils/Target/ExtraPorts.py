
class ExtraPorts(object):

    def __init__(self, count, state):
        self.count = count
        self.state = state

    @staticmethod
    def fromNode(node):
        count = node.attrib['count']
        state = node.attrib['state']
        return ExtraPorts(count, state)
