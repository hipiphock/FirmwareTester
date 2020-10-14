"""
There are three classes here: Cluster, Attribute, Command.

Class들을 만들어서 해당 class를 추가하고 마는 식으로 구현

Cluster의 member로
 - Attribute
 - Command

Dictionary로 만드는게 나을까? 이름, id 형식으로
"""
from constants import *

class Cluster:
    """
    Each cluster should have cluster name, and cluster number.
    """
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.id = id
        self.attr_list = []
        self.cmd_list = []

    def addAttribute(self, attr):
        self.attr_list.append(attr)

    def removeAttribute(self, attr_id):
        for attr in self.attr_list:
            if attr.id == attr_id:
                self.attr_list.remove(attr)
                return
        # TODO: implement not found error

    def addCommand(self, cmd):
        self.cmd_list.append(cmd)

    def removeCommand(self, cmd_id):
        for cmd in self.cmd_list:
            if cmd.id == cmd_id:
                self.cmd_list.remove(cmd)
                return
        # TODO: implement not found error

    def readClusterFile(self, filename):
        pass

    def writeClusterFile(self, filename):
        pass


class Attribute:
    def __init__(self, id, name, min=None, max=None):
        self.id = id
        self.name = name
        # Add cluster id?
        self.min = min
        self.max = max

class Command:
    def __init__(self, id, name, payload=None):
        self.id = id
        self.name = name
        self.payload = None
    
    # TODO: need to do something with payload

def test():
    on_off_cluster = Cluster(ON_OFF_CLUSTER, "ON_OFF_CLUSTER")
    on_off_attr = Attribute(ON_OFF_ONOFF_ATTR, "ON_OFF_ONOFF_ATTR")
    toggle_cmd = Command(ON_OFF_TOGGLE_CMD, "ON_OFF_TOGGLE_CMD")
    on_off_cluster.addAttribute(on_off_attr)
    on_off_cluster.removeAttribute(ON_OFF_ONOFF_ATTR)
    on_off_cluster.addCommand(toggle_cmd)
    on_off_cluster.removeCommand(ON_OFF_TOGGLE_CMD)

if __name__ == "__main__":
    test()