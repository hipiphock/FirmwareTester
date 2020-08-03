import os

def isValidRange(val):
    if 0 < val < 65279:
        return True
    else:
        return False

PADDING_FOR_TIME = 0.2
PADDING_FOR_VALUE = 50 

def determine_ok(input_value, output_value):
    
    pass

def analyze_result(log_path, gui):
    with open(log_path, 'r') as f:
        lines = f.readlines()[1:]
        for line in lines:
            origin_line = line.split('\n')[0]
            line = line.split('\n')[0].split(';')
            
            if 'COLOR_CTRL' == line[1]: # color ctrl
                input_cmd = line[2]
                input_val = int(line[3].split(',')[0][2:])
                input_duration = float(line[3].split(',')[2][2:]) * 0.1
                interval = float(line[4])
                output_val = int(line[5])
                
                if input_val == output_val : # OK
                    gui.list_result.addItem(origin_line + " \tOK")
                else:
                    if interval > input_duration: # enough to transit color or temperature to the target point
                        if (interval - input_duration) <= PADDING_FOR_TIME:
                            gui.list_result.addItem(origin_line + " \t Error : The interval value may be short compared to the transition time.")
                        elif (abs(output_val - input_val) <= PADDING_FOR_VALUE):
                            gui.list_result.addItem(origin_line + " \tError : The distance between the input value and the output value is too far for the given transition time.")
                    else:   # short to transit color or temperature to the target point
                        gui.list_result.addItem(origin_line + " \tError : The interval value may be short compared to the transition time.")
            elif 'LVL_CTRL' == line[1]: # color ctrl
                input_cmd = line[2]
                input_val = int(line[3].split(',')[0][2:])
                input_duration = float(line[3].split(',')[2][2:]) * 0.1
                interval = float(line[4])
                output_val = int(line[5])
                
                if input_val == output_val : # OK
                    gui.list_result.addItem(origin_line + "\tOK")
                else:
                    if interval > input_duration: # enough to transit color or temperature to the target point
                        if (interval - input_duration) <= PADDING_FOR_TIME:
                            gui.list_result.addItem(origin_line + "\t Error : The interval value may be short compared to the transition time.")
                        elif (abs(output_val - input_val) <= PADDING_FOR_VALUE): # change to abs(previous output - current input)
                            gui.list_result.addItem(origin_line + " \tError : The distance between the input value and the output value is too far for the given transition time.")
                    else:   # short to transit color or temperature to the target point
                        gui.list_result.addItem(origin_line + "\tError : The interval value may be short compared to the transition time.")
            elif 'ON_OFF' == line[1]:
                input_cmd = line[2]
                input_val = "True" if input_cmd == "ON" else "False"  
                input_duration = 0.1
                interval = float(line[4])
                output_val = line[5]
              
                if input_val == output_val : # OK
                    gui.list_result.addItem(origin_line + " \tOK")
                else:
                    if interval > input_duration: # enough to transit color or temperature to the target point
                        if (interval - input_duration) <= PADDING_FOR_TIME:
                            gui.list_result.addItem(origin_line + " \t Error : The interval value may be short compared to the transition time.")
                        elif (abs(output_val - input_val) <= PADDING_FOR_VALUE):
                            gui.list_result.addItem(origin_line + " \tError : The distance between the input value and the output value is too far for the given transition time.")
                    else:   # short to transit color or temperature to the target point
                        gui.list_result.addItem(origin_line + " \tError : The interval value may be short compared to the transition time.")

    gui.list_result.addItem("---------------------------------")
        