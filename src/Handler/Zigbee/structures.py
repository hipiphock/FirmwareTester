"""
name    = key
id      = value
"""
import os
import sys
import json
from collections import OrderedDict
from zb_cli_wrapper.src.utils.zigbee_classes.clusters.attribute import Attribute

class Attr:
    def __init__(self, id, name, desc, attr_type, min=None, max=None):
        self.id = id
        self.name = name
        self.desc = desc
        self.type = attr_type
        self.min = min
        self.max = max

class Cmd:
    def __init__(self, id, name, desc, affected_attrs=None):
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
                attr_obj = Attr(int(attr['id'], 16), attr['name'], attr['desc'], int(attr['type'], 16))
                attr_table[attr['name']] = attr_obj
            cmd_table = {}
            for cmd in cluster['commands']:
                cmd_obj = Cmd(int(cmd['id'], 16), cmd['name'], cmd['desc'], cmd['affected_attrs'])
                cmd_table[cmd['name']] = cmd_obj
            return cls(cluster['id'], cluster['name'], attr_table, cmd_table)

    def writeClusterFile(self, filename):
        with open(filename, "w", encoding="utf-8") as cluster_file:
            json_to_write = {}
            json_to_write['id'] = self.id
            json_to_write['name'] = self.name
            json_to_write['attributes'] = []
            json_to_write['commands'] = []
            # case: initial clusters - they do not have attrs or cmds
            if self.attr_table is None or self.cmd_table is None:
                json.dump(json_to_write, cluster_file, ensure_ascii=False, indent="\t")
                return

            for attr_key in self.attr_table:
                attr_id = str(hex(self.attr_table[attr_key].id))
                attr_name = self.attr_table[attr_key].name
                attr_desc = self.attr_table[attr_key].desc
                attr_type = str(hex(self.attr_table[attr_key].type))
                json_to_write['attributes'].append({
                    'id':   attr_id,
                    'name': attr_name,
                    'desc': attr_desc,
                    'type': attr_type
                })
            # command
            for cmd_key in self.cmd_table:
                cmd_id = str(hex(self.cmd_table[cmd_key].id))
                cmd_name = self.cmd_table[cmd_key].name
                cmd_desc = self.cmd_table[cmd_key].desc
                affected_attrs = self.cmd_table[cmd_key].affected_attrs
                json_to_write['commands'].append({
                    'id':cmd_id,
                    'name':cmd_name,
                    'desc':cmd_desc,
                    'affected_attrs':affected_attrs
                })
            json.dump(json_to_write, cluster_file, ensure_ascii=False, indent="\t")


class TaskCmd(Cmd):
    def __init__(self, cmd, payloads=None, waittime=20.0):
        super().__init__(cmd.id, cmd.name, cmd.desc, cmd.affected_attrs)
        self.payloads = payloads
        self.waittime = waittime
        

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

def update_cluster_table():
    global CLUSTER_TABLE, CLUSTER_FILE_TABLE
    CLUSTER_TABLE, CLUSTER_FILE_TABLE = get_all_clusters()