import serial
import sys
import json

def serial_ports():   
    """ Lists serial port names   
       
        :raises EnvironmentError:   
            On unsupported or unknown platforms   
        :returns:   
            A list of the serial ports available on the system   
    """   
    if sys.platform.startswith('win'):   
        ports = ['COM%s' % (i + 1) for i in range(256)]   
    else:   
        raise EnvironmentError('Unsupported platform')   

    result = []   
    for port in ports:   
        try:   
            s = serial.Serial(port)
            s.close()   
            result.append(port)   
        except:   
            pass   
    return result   



def read_command_from_json(file_name, module_index):
    with open(file_name) as json_file:
        json_data = json.load(json_file)
        list = []
        if module_index == 0:  # Zigbee HA
            if "iteration" in json_data:  # routine 의 경우
                list.append("routine, " + str(json_data["iteration"]))
                for item in json_data["task_list"]:
                    command_type = item.split("\\")[-1].split("_")
                    if command_type[0] == "on.json" or command_type[0] == "off.json":
                        list.append("on/off, " + command_type[0].split(".")[0])
                    else:
                        list.append(command_type[0] + ", " + command_type[-1].split(".")[0])
            elif "commands" in json_data:  # single command 의 경우
                for item in json_data["commands"]:
                    task_kind = item["task_kind"]
                    cluster = item["cluster"]
                    command_string = ""
                    if cluster == ON_OFF_CLUSTER:
                        if task_kind == 0:
                            command = item["command"]
                            command_string = "on/off, " + str(command)
                        else:
                            attr_id = item["attr_id"]
                            command_string = "read attribute, " + zigbee_attr_to_str[cluster][attr_id]
                    elif cluster == COLOR_CTRL_CLUSTER:
                        if task_kind == 0:
                            payloads = item["payloads"]
                            command_string = "color, " + str(payloads[0][0])
                        else:
                            attr_id = item["attr_id"]
                            command_string = "read attribute, " + zigbee_attr_to_str[cluster][attr_id]
                    elif cluster == LVL_CTRL_CLUSTER:
                        if task_kind == 0:
                            payloads = item["payloads"]
                            command_string = "level, " + str(payloads[0][0])
                        else:
                            attr_id = item["attr_id"]
                            command_string = "read attribute, " + zigbee_attr_to_str[cluster][attr_id]
                    list.append(command_string)
        return list
