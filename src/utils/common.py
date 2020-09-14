'''
    this file has general function and variables which are used in this program
'''
from enum import Enum


class PageNumber(Enum):
    ZIGBEE_HA = 2
    BLE = 3
    BLE_MESH = 4

    def __int__(self):
        return self.value