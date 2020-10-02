import time

from serial.serialutil import SerialTimeoutException
from zb_cli_wrapper.zb_cli_dev import ZbCliDevice
from zb_cli_wrapper.src.utils.zigbee_classes.clusters.attribute import Attribute

class ZigBeeDriver():
    def __init__(self, port, channel, target_id):
        self.target_id = target_id
        self.channel = channel
        self.port = port
        self.cli_instance = ZbCliDevice('', '', port)
        self.short = None

    def get_short_address(self):
        self.short = 'short address'

    def connect(self):
        try:
            if not self.short:
                self.cli_instance.bdb.channel = [self.channel]
                self.cli_instance.bdb.role = 'zr' # zigbee router
                self.cli_instance.bdb.start()
                self.get_short_address()    
                
            return self.short

        except SerialTimeoutException:
            print("connect failed: {}".format('Write timeout'))

