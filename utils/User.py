
from println import println, printText

class User(object):

    def __init__(self, name, role, printField):
        assert name != None
        assert role != None
        self.name = name
        self.role = self.roleType(role)
        self.printField = printField
        printText(self.printField, 'User: %s with role: %s loggin.' % (self.name, self.role))

    def roleType(self, role):
        text = role.lower()
        if 'ex' in role or 'exploit' in role:
            return 'Exploit'
        elif 'an' in role or 'analysis' in role:
            return 'Analysis'
        elif 'de' in role or 'defense' in role:
            return 'Defense'
        else:
            return 'None'

    def getUserName(self):
        return self.name

    def getRole(self):
        return self.role
