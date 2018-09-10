
import xml.etree.ElementTree as ET

from utils.println import printText

def parse(analysis, redis, printField, path):
    if path == 'parse':
        pass
    else:
        printText(printField, 'Parseing: %s' % path)
        tree = ET.parse(path)
        root = tree.getroot()
        host = root.find('host')
        ports = []
        for each in host.find('ports'):
            ports.append(each)
            #service = each[]
        printText(printField, 'Parse completed.')
    return 'Parse'
