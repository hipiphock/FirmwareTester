"""
There are three classes here: Cluster, Attribute, Command.

Class들을 만들어서 해당 class를 추가하고 마는 식으로 구현

Cluster의 member로
 - Attribute
 - Command

Dictionary로 만드는게 나을까? 이름, id 형식으로
"""
import os
import sys
import json 
from constants import *

class Cluster:
    """
    Each cluster should have cluster name, and cluster number.
    """
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.id = id
        self.attr_table = {}
        self.cmd_table = {}

    def addAttr(self, attr_key, attr):
        self.attr_table[attr_key] = attr

    def removeAttr(self, attr_key):
        del self.attr_table[attr_key]

    def addCmd(self, cmd_key, cmd):
        self.cmd_table[cmd_key] = cmd

    def removeCmd(self, cmd_key):
        del self.cmd_table[cmd_key]

    def readClusterFile(self, filename):
        # TODO: read cluster files
        with open(filename, "r") as cluster_file:
            cluster = json.load(cluster_file)
            print(cluster)
        

    def writeClusterFile(self, filename):
        pass

# returns cluster files' name
def get_all_clusters():
    cluster_path = os.path.join(os.path.dirname(__file__), 'Clusters')
    cluster_list = [f for f in os.listdir(cluster_path) if os.path.isfile(os.path.join(cluster_path, f))]
    return cluster_list

class Attr:
    def __init__(self, id, name, min=None, max=None):
        self.id = id
        self.name = name
        # Add cluster id?
        self.min = min
        self.max = max

class Cmd:
    def __init__(self, id, name, payload=None):
        self.id = id
        self.name = name
        self.payload = None
    
    # TODO: need to do something with payload

def test():
    cluster_list = get_all_clusters()
    for cluster in cluster_list:
        print(cluster)
    on_off_cluster = Cluster(ON_OFF_CLUSTER, "ON_OFF_CLUSTER")
    on_off_attr = Attr(ON_OFF_ONOFF_ATTR, "ON_OFF_ONOFF_ATTR")
    toggle_cmd = Cmd(ON_OFF_TOGGLE_CMD, "ON_OFF_TOGGLE_CMD")
    on_off_cluster.addAttr('ON_OFF_ATTR', on_off_attr)
    on_off_cluster.removeAttr('ON_OFF_ATTR')
    on_off_cluster.addCmd('ON_OFF_TOGGLE_CMD', toggle_cmd)
    on_off_cluster.removeCmd("ON_OFF_TOGGLE_CMD")

if __name__ == "__main__":
    test()