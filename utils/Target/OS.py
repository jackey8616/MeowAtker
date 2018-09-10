
class OS(object):

    def __init__(self, osMatch):
        self.osMatch = osMatch

    @staticmethod
    def fromNode(node):
        osMatch = []
        for each in node.findall('osmatch'):
            osMatch.append(OSMatch(each))
        return OS(osMatch)

class OSMatch(object):

    def __init__(self, name, accuracy, osClass):
        self.name = name
        self.accuracy = accuracy
        self.osClass = osClss

    @staticmethod
    def fromNode(node):
        name = node.attrib['name']
        accuracy = node.attrib['accuracy']
        osClass = OSClass(node.find('osclass'))
        return OSMatch(name, accuracy, osClass)

class OSClass(object):

    def __init__(self, osType, osFamily, vendor, osGen, accuracy):
        self.osType = osType
        self.osFamily = osFamily
        self.vendor = vendor
        self.osGen = osGen
        self.accuracy = accuracy

    @staticmethod
    def fromNode(node):
        osType = node.attrib['type']
        osFamily = node.attrib['osfamily']
        vendor = node.attrib['vendor']
        osGen = node.attrib['osgen']
        accuracy = node.attrib['accuracy']
        return OSClass(osType, osFamily, vendor, osGen, accuracy)
