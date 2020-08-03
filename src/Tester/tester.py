# from context import DongleHandler
from DongleHandler import *
import logging
import random
import os
# This is basic test on Ultra Thin Wafer by Samsung Electronics.
def Tester(device_file, commands, port, iter_count, gui):
    # for logging
    # logging.basicConfig(level=logging.DEBUG)
    if type(device_file) is dict:
        device = Device(device_file['name'], 0, device_file['eui64'], device_file['ep'])
    else:
        device = parse_json_device(device_file)

    sample_task_list = parse_task_list(commands)
    task_routine = TaskRoutine(device, 0, sample_task_list, port, iter_count, gui)
    log_name = task_routine.start_routine()
    return log_name