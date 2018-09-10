
import xml.etree.ElementTree as ET
from Host import Host

class Target(object):

    def __init__(self, tree, root, host):
        self.tree = tree
        self.root = root
        self.host = host

    @staticmethod
    def newByXMLFile(path):
        tree = ET.parse(path)
        root = tree.getroot()
        host = []
        for each in root.findall('host'):
            host.append(Host.fromNode(each))
        return Target(tree, root, host)

    @staticmethod
    def newByXMLNode(node):
        pass

