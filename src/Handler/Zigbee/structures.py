"""
name    = key
id      = value
"""
import os
import sys
import json 
from constants import *

class Cluster:
    """
    Each cluster should have cluster name, and cluster number.
    """
    def __init__(self, id, name, attr_table=None, cmd_table=None):
        super().__init__()
        self.id = id
        self.name = name
        self.attr_table = attr_table
        self.cmd_table = cmd_table

    def addAttr(self, attr_key, attr):
        if self.attr_table == None:
            self.attr_table = {}
        self.attr_table[attr_key] = attr

    def removeAttr(self, attr_key):
        del self.attr_table[attr_key]

    def addCmd(self, cmd_key, cmd):
        if self.cmd_table == None:
            self.cmd_table = {}
        self.cmd_table[cmd_key] = cmd

    def removeCmd(self, cmd_key):
        del self.cmd_table[cmd_key]

    @classmethod
    def readClusterFile(cls, filename):
        with open(filename, "r") as cluster_file:
            cluster = json.load(cluster_file)
            # need to handle attr_table and cmd_table
            attr_table = {}
            for attr in cluster['attributes']:
                attr_type = attr['type']    # TODO: convert element to attribute type
                attr_obj = Attr(attr['id'], attr['name'], attr_type)
                attr_table[attr['name']] = attr_obj
            cmd_table = {}
            for cmd in cluster['commands']:
                print(cmd)
                cmd_obj = Cmd(cmd['id'], cmd['name'])
                cmd_table[cmd['name']] = cmd_obj
            return cls(cluster['id'], cluster['name'], attr_table, cmd_table)

    def writeClusterFile(self, filename):
        pass


class Attr:
    def __init__(self, id, name, attr_type, min=None, max=None):
        self.id = id
        self.name = name
        self.type = attr_type
        self.min = min
        self.max = max


class Cmd:
    def __init__(self, id, name, payload=None):
        self.id = id
        self.name = name
        self.payload = None
    # TODO: need to do something with payload


class TaskCmd:
    # class that is going to be used in main routine
    def __init__(self, cluster_key, command_key, attrs):
        self.cluster_key = cluster_key
        self.command_key = command_key
        self.attrs = attrs
    
    # get attribute lists
    def getAttrList(self):
        for attr in self.attrs:
            # TODO: how do I find cluster?
            pass


# returns cluster files' name
def get_all_clusters():
    cluster_path = os.path.join(os.path.dirname(__file__), 'Clusters')
    cluster_file_list = [f for f in os.listdir(cluster_path) if os.path.isfile(os.path.join(cluster_path, f))]
    cluster_table = {}
    for cluster_file in cluster_file_list:
        # read each cluster file, and save it to cluster table
        cluster = Cluster.readClusterFile(os.path.join(cluster_path, cluster_file))
        cluster_table[cluster.name] = cluster
    return cluster_table

# FIXING
CLUSTER_TABLE = get_all_clusters()


def test():
    pass

if __name__ == "__main__":
    test()