

class Port(object):

    def __init__(self, protocol, portid, state, service):
        self.protocol = protocol
        self.portid = portid
        self.state = state
        self.service = service

    @staticmethod
    def fromNode(node):
        protocol = node.attrib['protocol']
        portid = node.attrib['portid']
        state = State.fromNode(node.find('state'))
        service = Service.fromNode(node.find('service'))
        return Port(protocol, portid, state, service)

class State(object):

    def __init__(self, reason, state, reasonTTL):
        self.reason = reason
        self.state = state
        self.reasonTTL = reasonTTL

    @staticmethod
    def fromNode(node):
        reason = node.attrib['reason']
        state = node.attrib['state']
        reasonTTL = node.attrib['reason_ttl']
        return State(reason, state, reasonTTL)

class Service(object):

    def __init__(self, product, name, extraInfo, version):
        self.product = product
        self.name = name
        self.extraInfo = extraInfo
        self.version = version

    @staticmethod
    def fromNode(node):
        product = node.attrib['product']
        name = node.attrib['name']
        extraInfo = node.attrib['extrainfo'] if 'extrainfo' in node.attrib else None
        version = node.attrib['version'] if 'version' in node.attrib else None
        return Service(product, name, extraInfo, version)
