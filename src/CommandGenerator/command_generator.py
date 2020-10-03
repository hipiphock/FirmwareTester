from Handler.Zigbee.zigbee_driver import ZigBeeDriver
from Handler.Zigbee import constants
from PyQt5.QtWidgets import *

class CmdGenerator():
    def __init__(self):
        pass

    def random_range(self, cmcd_type, isNormal):
        if isNormal:
            pass
        else:
            pass
    
    def cmd_connect(self, **params):
        cmd = {}
        cmd['cluster'] = None
        
        if params['enabled']:
            cmd['command'] = 'CONNECT'
            cmd['CHANNEL'] = params['channel']
            cmd['PORT'] = params['port']
            
        return cmd

    def cmd_disconnect(self, **params):
        cmd = {}
        cmd['cluster'] = None

        if params['enabled']:
            cmd['command'] = 'DISCONNECT'
        
        return cmd

    def cmd_onoff(self, **params):
        cmd = {}
        cmd['cluster'] = 'ON_OFF_CLUSTER'

        if params['on']:
            cmd['command'] = 'ON'
        elif params['off']:
            cmd['command'] = 'OFF'            
        elif params['toggle']:
            cmd['command'] = 'TOGGLE'
        cmd['payloads'] = None
        return cmd


    def cmd_level_inteface(self, command, layout):
        params = {}
        params['command'] = command

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

                        if isinstance(widget, QRadioButton):
                            if widget.objectName() == "radio_normal" and widget.isChecked() :
                                pass # get value from normal range
                            if widget.objectName() == "radio_abnormal" and widget.isChecked() :
                                pass # get value from abnormal range
            if params['transition'] >= params['wait']:
                params['wait'] = params['transition'] + 1

        elif command == "STOP":
            pass

        return self.cmd_level(params=params)

    def cmd_level(self, params):
        cmd = {}
        cmd['cluster'] = 'LVL_CTRL_CLUSTER'
        cmd['command'] = params['command']

        if cmd['command'] == 'MOVE_TO' or cmd['command'] == 'MOVE_TO_ONOFF':
            level = (params['level'], constants.TYPES.UINT8)
            transition = (params['transition'], constants.TYPES.UINT16)
            cmd['payloads'] = [level, transition]
        
        elif cmd['command'] == 'STOP':
            cmd['payloads'] = None

        cmd['wait'] = params['wait']
        
        return cmd

    def cmd_color_inteface(self, command, layout):
        params = {}
        params['command'] = command

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

                        if isinstance(widget, QRadioButton):
                            if widget.objectName() == "radio_normal" and widget.isChecked() :
                                pass # get value from normal range
                            if widget.objectName() == "radio_abnormal" and widget.isChecked() :
                                pass # get value from abnormal range
                    
            if params['transition'] >= params['wait']:
                params['wait'] = params['transition'] + 1

        elif command == "MOVE_TO_COLOR":
            for child in layout:
                if isinstance(child, QHBoxLayout):  # start of row
                    for i in range(child.count()):
                        widget = child.itemAt(i).widget()
                        if widget.objectName() == "lineEdit_color_x":
                            params['color_x'] = widget.value()      
                        elif widget.objectName() == "lineEdit_color_y":
                            params['color_y'] = widget.value()        
                        elif widget.objectName() == "spinbox_transition":
                            params['transition'] = widget.value()   
                        elif widget.objectName() == "spinbox_wait":
                            params['wait'] = widget.value()

                        if isinstance(widget, QRadioButton):
                            if widget.objectName() == "radio_normal" and widget.isChecked() :
                                pass # get value from normal range
                            if widget.objectName() == "radio_abnormal" and widget.isChecked() :
                                pass # get value from abnormal range
                    
            if params['transition'] >= params['wait']:
                params['wait'] = params['transition'] + 1


        return self.cmd_color(params=params)

    def cmd_color(self, params):
        cmd = {}
        cmd['cluster'] = 'COLOR_CTRL_CLUSTER'
        cmd['command'] = params['command']

        if cmd['command'] == 'MOVE_TO_MIRED':
            mired = (params['mired'], constants.TYPES.UINT16)
            transition = (params['transition'], constants.TYPES.UINT16)
            cmd['payloads'] = [mired, transition]
            cmd['wait'] = params['wait']

        elif cmd['command'] == 'MOVE_TO_COLOR':
            color_x = (params['x'], constants.TYPES.UINT16)
            color_y = (params['y'], constants.TYPES.UINT16)
            transition = (params['transition'], constants.TYPES.UINT16)

            cmd['payloads'] = [color_x, color_y, transition]
            cmd['wait'] = params['wait']
            
        return cmd
