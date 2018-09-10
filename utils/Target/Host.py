
from Port import Port
from ExtraPorts import ExtraPorts
from OS import OS

class Host(object):

    def __init__(self, status, address, hostnames, ports, os, uptime):
        self.status = status
        self.address = address
        self.hostnames = hostnames
        self.ports = ports
        self.os = os
        self.uptime = uptime

    @staticmethod
    def fromNode(node):
        status = node.find('status').attrib['state']
        address = node.find('address').attrib['addr']
        hostnames = None
        ports = []
        for each in node.find('ports'):
            if each.tag == 'port':
                innerNode = Port.fromNode(each)
            elif each.tag == 'extraports':
                innerNode = ExtraPorts.fromNode(each)
            ports.append(innerNode)
        os = OS.fromNode(node.find('os'))
        uptime = None
        return Host(status, address, hostnames, ports, os, uptime)
