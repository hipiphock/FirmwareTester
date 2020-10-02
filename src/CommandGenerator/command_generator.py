from Handler.Zigbee.zigbee_driver import ZigBeeDriver
from Handler.Zigbee import constants

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
        if params['enabled']:
            cmd['command'] = 'CONNECT'
            cmd['CHANNEL'] = params['channel']
            cmd['PORT'] = params['port']
            
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

        return cmd

    def cmd_level(self, **params):
        cmd = {}
        cmd['cluster'] = 'LVL_CTRL_CLUSTER'

        cmd['command'] = params['command']

        if cmd['command'] == 'MOVE_TO':
            level = (params['level'], constants.TYPES.UINT8)
            transition = (params['transition'], constants.TYPES.UINT16)
            cmd['payloads'] = [level, transition]
        
        elif cmd['command'] == 'STOP':
            pass
        
        elif cmd['command'] == 'MOVE_TO_ONOFF':
            level = (params['level'], constants.TYPES.UINT8)
            transition = (params['transition'], constants.TYPES.UINT16)
            cmd['payloads'] = [level, transition]
            cmd['wait'] = params['wait']
        
        return cmd

    def cmd_color(self, **params):
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
