import time

from serial.serialutil import SerialTimeoutException
from zb_cli_wrapper.zb_cli_dev import ZbCliDevice
from zb_cli_wrapper.src.utils.communicator import CommandError
from zb_cli_wrapper.src.utils.zigbee_classes.clusters.attribute import Attribute
from Handler.Zigbee.constants import DEFAULT_ZIGBEE_PROFILE_ID, clusters, commands, attributes, ON_OFF_CLUSTER, LVL_CTRL_CLUSTER, COLOR_CTRL_CLUSTER

class ZigBeeDriver():
    def __init__(self, port, channel, target_id):
        self.target_id = target_id
        self.channel = channel
        self.port = port
        self.cli_instance = ZbCliDevice('', '', port)
        self.short = None
        self.entry_point = 8
    
    def __del__(self):
        self.cli_instance.close_cli()

    def get_short_address(self):
        try:
            self.short = self.cli_instance.zdo.short_addr
            return self.short
    
        except CommandError:
            print("device was not commissioned")
            return -1
        
    def connect(self):
        try:
            self.cli_instance.bdb.channel = [self.channel]
            self.cli_instance.bdb.role = 'zr' # zigbee router
            self.cli_instance.bdb.start()
            
            return self.get_short_address()    
                
        except SerialTimeoutException:
            print("connect failed: {}".format('Write timeout'))
        
        except CommandError: # already connected
            try:
                self.cli_instance.bdb.start()
            except CommandError:
                pass
            return self.get_short_address()
    
    def disconnect(self):
        self.cli_instance.bdb.factory_reset()
        self.short = None
        
        return self.get_short_address()

    def write_attr_command(self, cmd):
        cluster = clusters[cmd['cluster']]

        if cluster == ON_OFF_CLUSTER:
            cmd_id = commands[cmd['cluster']][cmd['command']]
        elif cluster == LVL_CTRL_CLUSTER:
            cmd_id = commands[cmd['cluster']][cmd['command']]
        elif cluster == COLOR_CTRL_CLUSTER:
            cmd_id = commands[cmd['cluster']][cmd['command']]


        self.cli_instance.zcl.generic(
            eui64=self.target_id,
            ep=self.entry_point,
            profile=DEFAULT_ZIGBEE_PROFILE_ID,
            cluster=cluster,
            cmd_id=cmd_id,
            payload=cmd['payloads']
        )
        try:
            time.sleep(cmd['wait'] / 1000) # waiting for the transition
        except KeyError:
            pass
        
    def read_attr_command(self, attribute):
        try:
            result = self.cli_instance.zcl.readattr(self.target_id, attr=attribute, ep=self.entry_point)
        except CommandError:
            print("request Timed out")
            
        return result
