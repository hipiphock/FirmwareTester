# from Handler.Zigbee.constants import DEFAULT_ZIGBEE_PROFILE_ID
# from Handler.Zigbee.zigbee_driver import ZigBeeDriver
# from CommandGenerator.command_generator import CmdGenerator
# from main import Worker
# import time

# zb = ZigBeeDriver('COM13', 19, int("88571DFFFE0E5408", 16))

# # command test
# zb.connect()
# print(zb.get_short_address())

# zb.disconnect()

# print(zb.get_short_address())

# cmd_gen = CmdGenerator()
# on = cmd_gen.cmd_onoff(on=True, off=False, toggle=False)
# move_to = cmd_gen.cmd_level(command='MOVE_TO', level=254, transition=65534)
# toggle = cmd_gen.cmd_onoff(on=False, off=False, toggle=True)
# zb.write_attr_command(on)
# time.sleep(1)
# zb.write_attr_command(move_to)
# time.sleep(1)
# zb.write_attr_command(toggle)

from CommandGenerator.command_generator import CmdGenerator
from Handler.Zigbee.zigbee_driver import ZigBeeDriver
from Handler.Zigbee.structures import CLUSTER_TABLE, TaskCmd

task_cmd_list = []
cmdgen = CmdGenerator()
zigbeedriver = ZigBeeDriver('COM14', 24, 9824354097448244232)
task_cmd_list.append(cmdgen.new_cmd('ON_OFF_CLUSTER', 'TOGGLE', None, 20))
task_cmd_list.append(cmdgen.new_cmd('ON_OFF_CLUSTER', 'TOGGLE', None, 20))
task_cmd_list.append(cmdgen.new_cmd('ON_OFF_CLUSTER', 'TOGGLE', None, 20))
for task_cmd in task_cmd_list:
    zigbeedriver.new_run_command(0, task_cmd)