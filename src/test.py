from Handler.Zigbee.constants import DEFAULT_ZIGBEE_PROFILE_ID
from Handler.Zigbee.zigbee_driver import ZigBeeDriver
from CommandGenerator.command_generator import CmdGenerator
from main import Worker
import time

zb = ZigBeeDriver('COM13', 19, int("88571DFFFE0E5408", 16))

# command test

# cmd_gen = CmdGenerator()
# on = cmd_gen.cmd_onoff(on=True, off=False, toggle=False)
# move_to = cmd_gen.cmd_level(command='MOVE_TO', level=254, transition=65534)
# toggle = cmd_gen.cmd_onoff(on=False, off=False, toggle=True)
# zb.write_attr_command(on)
# time.sleep(1)
# zb.write_attr_command(move_to)
# time.sleep(1)
# zb.write_attr_command(toggle)

