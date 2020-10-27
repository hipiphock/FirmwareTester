"""
name    = key
id      = value
"""
import os
import sys
import json
from zb_cli_wrapper.src.utils.zigbee_classes.clusters.attribute import Attribute

class Attr:
    def __init__(self, id, name, attr_type, min=None, max=None):
        self.id = id
        self.name = name
        self.type = attr_type
        self.min = min
        self.max = max

class Cmd:
    def __init__(self, id, name, desc, affected_attrs):
        self.id = id
        self.name = name
        self.desc = desc
        self.affected_attrs = affected_attrs

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
        cmd = cmd

    def removeCmd(self, cmd_key):
        del cmd

    @classmethod
    def readClusterFile(cls, filename):
        with open(filename, "r") as cluster_file:
            cluster = json.load(cluster_file)
            # need to handle attr_table and cmd_table
            attr_table = {}
            for attr in cluster['attributes']:
                attr_obj = Attr(int(attr['id'], 16), attr['name'], int(attr['type'], 16))
                attr_table[attr['name']] = attr_obj
            cmd_table = {}
            for cmd in cluster['commands']:
                cmd_obj = Cmd(int(cmd['id'], 16), cmd['name'], cmd['desc'], cmd['affected_attrs'])
                cmd_table[cmd['name']] = cmd_obj
            return cls(cluster['id'], cluster['name'], attr_table, cmd_table)

    def writeClusterFile(self, filename):
        with open(filename, "w") as cluster_file:
            json_to_write = {}
            json_to_write['id'] = self.id
            json_to_write['name'] = self.name
            # attribute
            json_to_write['attributes'] = []
            for attr_key in self.attr_table:
                attr_id = self.attr_table[attr_key].id
                attr_name = self.attr_table[attr_key].name
                attr_type = self.attr_table[attr_key].type
                json_to_write['attributes'].append({
                    'id':attr_id,
                    'name':attr_name,
                    'type':attr_type
                })
            # command
            json_to_write['commands'] = []
            for cmd_key in self.cmd_table:
                cmd_id = self.cmd_table[cmd_key].id
                cmd_name = self.cmd_table[cmd_key].name
                cmd_desc = self.cmd_table[cmd_key].desc
                affected_attrs = self.cmd_table[cmd_key].affected_attrs
                json_to_write['commands'].append({
                    'id':cmd_id,
                    'name':cmd_name,
                    'desc':cmd_desc,
                    'affected_attrs':affected_attrs
                })
            json.dump(json_to_write, cluster_file)

class TaskCmd:
    # class that is going to be used in main routine
    def __init__(self, cluster_key, command_key, attrs, payloads=None):
        self.cluster_key = cluster_key
        self.cluster_id = CLUSTER_TABLE[cluster_key]
        self.command_key = command_key
        self.command_id = CLUSTER_TABLE[cluster_key]['commands'][command_key]['id']
        self.attr_list = []
        for attr in attrs:
            attr = CLUSTER_TABLE[cluster_key]['attributes'][attr]
            self.attr_list.append(Attribute(CLUSTER_TABLE[cluster_key]['id'], id=attr['id'], type=attr['type']))
        self.payloads = payloads

# returns cluster files' name
def get_all_clusters():
    cluster_path = os.path.join(os.path.dirname(__file__), 'Clusters')
    cluster_file_list = [f for f in os.listdir(cluster_path) if os.path.isfile(os.path.join(cluster_path, f))]
    cluster_table = {}
    cluster_file_table = {}
    for cluster_file in cluster_file_list:
        # read each cluster file, and save it to cluster table
        cluster_file_path = os.path.join(cluster_path, cluster_file)
        cluster = Cluster.readClusterFile(cluster_file_path)
        cluster_table[cluster.name] = cluster
        cluster_file_table[cluster.name] = cluster_file_path
    return cluster_table, cluster_file_table

# FIXING
CLUSTER_TABLE, CLUSTER_FILE_TABLE = get_all_clusters()

# for test
# if __name__ == "__main__":
#     attr_table = []
#     for i in range(5):
#         test = Attr(99, 'test', 99)
#         attr_table.append(test)
#     cmd_table = []
#     for i in range(5):
#         test = Cmd(99, 'test', 'for test', ['test', 'test'])
#         cmd_table.append(test)
#     test = Cluster(99, 'test', attr_table=attr_table, cmd_table=cmd_table)
#     test.writeClusterFile("test.json")