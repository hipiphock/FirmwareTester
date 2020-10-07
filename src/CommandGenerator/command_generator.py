import datetime
import random

from Handler.Zigbee.zigbee_driver import ZigBeeDriver
from Handler.Zigbee import constants
from PyQt5.QtWidgets import *


class CmdGenerator():
    def __init__(self):
        pass

    def get_random_value(self, cluster, command, isNormal):
        if command == 'MOVE_TO' or command =="MOVE_TO_ONOFF":
            if isNormal:
                return random.randint(1, 255)
            else:
                abnormal_range = []
                under = random.randint(0 ,1)
                over = random.randint(255, 999)

                abnormal_range.append(under)
                abnormal_range.append(over)

                return random.choice(abnormal_range)

        elif command == "MOVE_TO_MIRED":
            if isNormal:
                return random.randint(200,371)
            else:
                abnormal_range = []
                under = random.randint(0, 200)
                over = random.randint(371, 999)

                abnormal_range.append(under)
                abnormal_range.append(over)

                return random.choice(abnormal_range)

        elif command == "MOVE_TO_COLOR":
            if isNormal:
                return random.randint(int('0x31E9', 16), int('0x7F87', 16))
            else:
                abnormal_range = []
                under = random.randint(int('0x0000', 16), int('0x31E9', 16))
                over = random.randint(int('0x7F88', 16), int('0xFFFF', 16))
                
                abnormal_range.append(under)
                abnormal_range.append(over)

                return random.choice(abnormal_range)


    def random_range(self, cmcd_type, isNormal):
        if isNormal:
            pass
        else:
            pass
    
    def cmd_connect(self, **params):
        cmd = {}
        cmd['cluster'] = None
        # cmd['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if params['enabled']:
            cmd['command'] = 'CONNECT'
            cmd['CHANNEL'] = params['channel']
            cmd['PORT'] = params['port']
            
        return cmd

    def cmd_disconnect(self, **params):
        cmd = {}
        cmd['cluster'] = None
        # cmd['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if params['enabled']:
            cmd['command'] = 'DISCONNECT'
        
        return cmd

    def cmd_onoff(self, **params):
        cmd = {}
        cmd['cluster'] = 'ON_OFF_CLUSTER'
        # cmd['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if params['on']:
            cmd['command'] = 'ON'
        elif params['off']:
            cmd['command'] = 'OFF'            
        elif params['toggle']:
            cmd['command'] = 'TOGGLE'
        cmd['payloads'] = None
        return cmd


    def cmd_level_interface(self, command, layout):
        params = {}
        params['command'] = command
        poped_values = []

        if command == "MOVE_TO" or command == "MOVE_TO_ONOFF":
            for child in layout:
                if isinstance(child, QHBoxLayout):  # start of row
                    for i in range(child.count()):
                        widget = child.itemAt(i).widget()
                        if widget.objectName() == "spinbox_brightness":
                            params['level'] = widget.value()        
                        elif widget.objectName() == "spinbox_transition":
                            params['transition'] = widget.value()   
                        elif widget.objectName() == "spinbox_wait":
                            params['wait'] = widget.value()

                        if isinstance(widget, QCheckBox):
                            if widget.objectName() == "checkbox_normal" and widget.isChecked() :
                                poped_values.append(self.get_random_value(cluster='LVL_CTRL_CLUSTER', 
                                                    command=command, 
                                                    isNormal=True
                                )) # get value from normal range
                            if widget.objectName() == "checkbox_abnormal" and widget.isChecked() :
                                poped_values.append(self.get_random_value(cluster='LVL_CTRL_CLUSTER', 
                                                    command=command, 
                                                    isNormal=False
                                )) # get value from abnormal range
                            if len(poped_values) > 0 :
                                print(poped_values)
                                params['level'] = random.choice(poped_values)
                            
            if params['transition'] >= params['wait']:
                params['wait'] = params['transition'] + 1

        elif command == "STOP":
            pass

        return self.cmd_level(params=params)

    def cmd_level(self, params):
        cmd = {}
        cmd['cluster'] = 'LVL_CTRL_CLUSTER'
        cmd['command'] = params['command']
        # cmd['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if cmd['command'] == 'MOVE_TO' or cmd['command'] == 'MOVE_TO_ONOFF':
            level = (params['level'], constants.TYPES.UINT8)
            transition = (params['transition'], constants.TYPES.UINT16)
            cmd['payloads'] = [level, transition]
        
        elif cmd['command'] == 'STOP':
            cmd['payloads'] = None

        cmd['wait'] = params['wait']
        
        return cmd

    def cmd_color_interface(self, command, layout):
        params = {}
        params['command'] = command
        poped_values = []

        if command == "MOVE_TO_MIRED":
            for child in layout:
                if isinstance(child, QHBoxLayout):  # start of row
                    for i in range(child.count()):
                        widget = child.itemAt(i).widget()
                        if widget.objectName() == "spinbox_mired":
                            params['mired'] = widget.value()        
                        elif widget.objectName() == "spinbox_transition":
                            params['transition'] = widget.value()   
                        elif widget.objectName() == "spinbox_wait":
                            params['wait'] = widget.value()

                        if isinstance(widget, QCheckBox):
                            if widget.objectName() == "checkbox_normal" and widget.isChecked() :
                                poped_values.append(self.get_random_value(cluster='COLOR_CTRL_CLUSTER', 
                                                    command=command, 
                                                    isNormal=True
                                )) # get value from normal range
                            if widget.objectName() == "checkbox_abnormal" and widget.isChecked() :
                                poped_values.append(self.get_random_value(cluster='COLOR_CTRL_CLUSTER', 
                                                    command=command, 
                                                    isNormal=False
                                ))
                            if len(poped_values) > 0:
                                params['mired'] = random.choice(poped_values)

            if params['transition'] >= params['wait']:
                params['wait'] = params['transition'] + 1

        elif command == "MOVE_TO_COLOR":
            for child in layout:
                if isinstance(child, QHBoxLayout):  # start of row
                    for i in range(child.count()):
                        widget = child.itemAt(i).widget()
                        if widget.objectName() == "lineEdit_color_x":
                            params['color_x'] = widget.text()      
                        elif widget.objectName() == "lineEdit_color_y":
                            params['color_y'] = widget.text()        
                        elif widget.objectName() == "spinbox_transition":
                            params['transition'] = widget.value()   
                        elif widget.objectName() == "spinbox_wait":
                            params['wait'] = widget.value()

                        if isinstance(widget, QRadioButton):
                            if widget.objectName() == "radio_normal" and widget.isChecked() :
                                poped_values.append(self.get_random_value(cluster='COLOR_CTRL_CLUSTER', 
                                                    command=command, 
                                                    isNormal=True
                                ))
                                poped_values.append(self.get_random_value(cluster='COLOR_CTRL_CLUSTER', 
                                                    command=command, 
                                                    isNormal=True
                                ))
                            if widget.objectName() == "radio_abnormal" and widget.isChecked() :
                                poped_values.append(self.get_random_value(cluster='COLOR_CTRL_CLUSTER', 
                                                    command=command, 
                                                    isNormal=False
                                ))
                                poped_values.append(self.get_random_value(cluster='COLOR_CTRL_CLUSTER', 
                                                    command=command, 
                                                    isNormal=False
                                ))
                            if len(poped_values) > 0:
                                params['color_x'] = random.choice(poped_values)
                                params['color_y'] = random.choice(poped_values)

            if params['transition'] >= params['wait']:
                params['wait'] = params['transition'] + 1


        return self.cmd_color(params=params)

    def cmd_color(self, params):
        cmd = {}
        cmd['cluster'] = 'COLOR_CTRL_CLUSTER'
        cmd['command'] = params['command']
        # cmd['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if cmd['command'] == 'MOVE_TO_MIRED':
            mired = (params['mired'], constants.TYPES.UINT16)
            transition = (params['transition'], constants.TYPES.UINT16)
            cmd['payloads'] = [mired, transition]
            cmd['wait'] = params['wait']

        elif cmd['command'] == 'MOVE_TO_COLOR':
            color_x = (int(params['color_x'], 16), constants.TYPES.UINT16)
            color_y = (int(params['color_y'], 16), constants.TYPES.UINT16)
            transition = (params['transition'], constants.TYPES.UINT16)

            cmd['payloads'] = [color_x, color_y, transition]
            cmd['wait'] = params['wait']
            
        return cmd
