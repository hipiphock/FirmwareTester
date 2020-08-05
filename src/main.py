import sys
import os
import json
import config
import common
import result_parser

from Tester.tester import *

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from DongleHandler import constants
from DongleHandler import *
from zb_cli_wrapper.zb_cli_dev import ZbCliDevice
from zb_cli_wrapper.src.utils.zigbee_classes.clusters.attribute import Attribute


ui_file = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'ui', 'main.ui'))

device_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'res', 'device'))

command_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'res', 'command'))

log_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'log'))


form_class = uic.loadUiType(ui_file)[0]

command_model = QStandardItemModel()


class WindowClass(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dict_device = {}
        # show enable ports
        enabled_ports = common.serial_ports()
        for port in enabled_ports:
            self.combo_port_select.addItem(port)

        # add command combo box
        for name, command in config.ONOFF_COMMAND_LIST.items():  # for on/off
            self.onoff_commands.addItem(name)

        for name, command in config.COLOR_COMMAND_LIST.items():  # for color
            self.color_commands.addItem(name)

        for name, command in config.LEVEL_COMMAND_LIST.items():  # for level
            self.level_commands.addItem(name)

        # register event handler of each objects
        # menubar import
        self.action_import_device.triggered.connect(self.func_import_device)
        self.action_import_command.triggered.connect(self.func_import_command)

        # save device as json file
        self.btn_dev_gen.clicked.connect(self.func_dev_gen_clicked)

        # create command
        self.btn_cmd_gen.clicked.connect(self.func_cmd_gen_clicked)

        # handle interface according to command
        self.onoff_commands.currentIndexChanged.connect(
            self.func_onoff_command_interface)
        self.color_commands.currentIndexChanged.connect(
            self.func_color_command_interface)
        self.level_commands.currentIndexChanged.connect(
            self.func_level_command_interface)

        # reset command list
        self.btn_cmd_reset.clicked.connect(self.func_cmd_reset_clicked)

        # save command list as json
        self.btn_cmd_save.clicked.connect(self.func_cmd_save_clicked)

        # handle commmand listview
        self.list_gen_cmd.itemDoubleClicked.connect(
        self.func_cmd_list_double_clicked)

        # for lineEdit in self.group_device.findChildren(QLineEdit):
        #     print(lineEdit.objectName())
        # self.btn_cmd_gen.clicked.connect(self.btn_cmd_gen_clicked)

        self.btn_test_start.clicked.connect(self.func_test_start_clicked)

        # initialize
        self.func_level_command_interface()
        self.func_color_command_interface()
    # menubar functions

    def func_import_device(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open File', './')
        if file_name[0]:
            with open(file_name[0]) as json_file:
                json_data = json.load(json_file)
                if json_data["module"] == "ZigBee HA":
                    module_index = self.combo_module_select.findText(
                        json_data["module"])
                    # self.combo_module_select.currentIndexChanged(module_index)
                    self.text_name.setText("wafer")
                    # self.text_uuid.setText(json_data["uuid"])
                    self.text_address.setText(json_data["eui64"])
                    self.text_entrypoint.setText(json_data["ep"])
                else:
                    QMessageBox.about(self, "장치 정보 불러오기 실패", "장치 파일이 아닙니다.")

    def func_import_command(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', './')
        if file_name[0]:
            input_command = common.read_command_from_json(
                file_name[0], self.cbo_module.currentIndex())
            if input_command:
                command_model.clear()
                for command in input_command:
                    self.add_command(command)
            else:
                QMessageBox.about(self, "명령 정보 가져오기 실패", "명령 파일이 아닙니다.")

    # device generate
    def func_dev_gen_clicked(self):

        self.dict_device['module'] = self.combo_module_select.currentText()
        self.dict_device['name'] = self.text_name.text()
        # dict_device['uuid'] = self.text_uuid.text()
        self.dict_device['eui64'] = self.text_address.text()
        self.dict_device['ep'] = self.text_entrypoint.text()

        self.device_file = os.path.join(
            device_path, self.dict_device['name'] + '.json')

        with open(self.device_file, 'w') as f:
            try:
                f.write(json.dumps(self.dict_device))
                QMessageBox.about(
                    self, "message", self.device_file + " is saved")
            except Exception:
                QMessageBox.about(self, "message", Exception)

    def func_layout_clear(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().close()
            layout.takeAt(i)

    # handling command interface
    def func_onoff_command_interface(self):
        print(self.onoff_commands.currentText())

    def func_color_command_interface(self):
        selected_command = self.color_commands.currentText()
        self.func_layout_clear(self.layout_color_payload)
        self.func_layout_clear(self.layout_color_payload2)

        if selected_command == "MOVE TO COLOR" or selected_command == "MOVE COLOR" or selected_command == "STEP COLOR":
            self.label_color_x = QLabel("Color X")
            self.spin_color_x = QSpinBox()
            self.label_color_y = QLabel("Color Y")
            self.spin_color_y = QSpinBox()

            self.layout_color_payload.addWidget(self.label_color_x)
            self.layout_color_payload.addWidget(self.spin_color_x)
    
            self.layout_color_payload.addWidget(self.label_color_y)
            self.layout_color_payload.addWidget(self.spin_color_y)

        elif selected_command == "MOVE TO COLOR & TEMPERATURE":
            self.label_temperature = QLabel("온도")
            self.spin_temperature = QSpinBox()

            self.layout_color_payload.addWidget(self.label_temperature)
            self.layout_color_payload.addWidget(self.spin_temperature)

        elif selected_command == "MOVE COLOR & TEMPERATURE" or selected_command == "STEP COLOR & TEMPERATURE":
            self.label_mood = QLabel("색감")
            self.comboBox_mood = QComboBox()
            self.comboBox_mood.addItem("Warm")
            self.comboBox_mood.addItem("Cold")
            
            if selected_command == "MOVE COLOR & TEMPERATURE":
                self.label_temperature_rate = QLabel("Rate")
            else:
                self.label_temperature_rate = QLabel("Step")

            self.spin_temperature_rate = QSpinBox()

            self.layout_color_payload.addWidget(self.label_mood)
            self.layout_color_payload.addWidget(self.comboBox_mood)

            self.layout_color_payload.addWidget(self.label_temperature_rate)
            self.layout_color_payload.addWidget(self.spin_temperature_rate)

            self.label_temperature_max = QLabel("최대 온도")
            self.spin_temperature_max = QSpinBox()
            self.label_temperature_min = QLabel("최소 온도")
            self.spin_temperature_min = QSpinBox()

            self.layout_color_payload2.addWidget(self.label_temperature_max)
            self.layout_color_payload2.addWidget(self.spin_temperature_max)

            self.layout_color_payload2.addWidget(self.label_temperature_min)
            self.layout_color_payload2.addWidget(self.spin_temperature_min)


        elif selected_command == "STOP MOVE STEP":
            pass


    def func_level_command_interface(self):
        selected_command = self.level_commands.currentText()
        self.func_layout_clear(self.layout_level_payload)

        if selected_command == "MOVE TO" or selected_command == "MOVE TO ONOFF":
            self.label_level = QLabel("밝기")
            self.lineEdit_brightness = QLineEdit()

            self.layout_level_payload.addWidget(self.label_level)
            self.layout_level_payload.addWidget(self.lineEdit_brightness)
            self.lineEdit_brightness.setPlaceholderText("0~254 사이의 밝기")
        

        elif selected_command == "MOVE" or selected_command == "MOVE ONOFF":
            self.label_level = QLabel("최대/최소")
            self.comboBox_minmax = QComboBox()
            self.comboBox_minmax.addItem("최대")
            self.comboBox_minmax.addItem("최소")

            self.layout_level_payload.addWidget(self.label_level)
            self.layout_level_payload.addWidget(self.comboBox_minmax)

        elif selected_command == "STEP" or selected_command == "STEP ONOFF":
            self.label_mode = QLabel("방향")
            self.comboBox_level_mode = QComboBox()
            self.comboBox_level_mode.addItem("증가")
            self.comboBox_level_mode.addItem("감소")
            self.label_level = QLabel("단계")
            self.spin_step = QSpinBox()
            self.spin_step.setMaximum(254)

            self.layout_level_payload.addWidget(self.label_mode)
            self.layout_level_payload.addWidget(self.comboBox_level_mode)
            self.layout_level_payload.addWidget(self.label_level)
            self.layout_level_payload.addWidget(self.spin_step)

        elif selected_command == "STOP" or selected_command == "STOP ONOFF":
            pass


    # command generate
    def func_cmd_gen_clicked(self):
        commands = []
        groups = self.tabWidget.currentWidget().findChildren(QGroupBox)
        for group in groups:
            if "onoff" in group.objectName():  # on/off
                for i in range(self.count_onoff.value()):
                    req_cmd = {}
                    req_cmd['cluster'] = ON_OFF_CLUSTER
                    req_cmd['command'] = config.ONOFF_COMMAND_LIST[self.onoff_commands.currentText(
                    )]
                    req_cmd['payloads'] = None
                    req_cmd['duration'] = config.DEFAULT_DURATION
                    req_cmd['task_kind'] = config.TASK_CMD
                    commands.append(req_cmd)

            elif "color" in group.objectName():  # color
                for i in range(self.count_color.value()):
                    req_cmd = {}
                    command = self.color_commands.currentText()

                    req_cmd['cluster'] = COLOR_CTRL_CLUSTER
                    req_cmd['command'] = config.COLOR_COMMAND_LIST[self.color_commands.currentText()]

                    if command == "MOVE TO COLOR" or command == "STEP COLOR":
                        value_x = (self.spin_color_x.value(), TYPES.UINT16)
                        value_y = (self.spin_color_y.value(), TYPES.UINT16)
                        transition_time = (int(self.transit_color.value()), TYPES.UINT16)
                        req_cmd['payloads'] = [value_x, value_y, transition_time]
                    
                    elif command == "MOVE COLOR":
                        value_x = (self.spin_color_x.value(), TYPES.UINT16)
                        value_y = (self.spin_color_y.value(), TYPES.UINT16)
                        req_cmd['payloads'] = [value_x, value_y]

                    elif command == "MOVE TO COLOR & TEMPERATURE":
                        temperature = (self.spin_temperature.value(), TYPES.UINT16)
                        transition_time = (int(self.transit_color.value()), TYPES.UINT16)
                        req_cmd['payloads'] = [temperature, transition_time]

                    elif command == "MOVE COLOR & TEMPERATURE" or command == "STEP COLOR & TEMPERATURE":
                        if self.comboBox_mood.currentText() == "Warm":
                            mood = (0x01, TYPES.MAP8)
                        else:
                            mood = (0x03, TYPES.MAP8)   
                        
                        rate = (self.spin_temperature_rate.value(), TYPES.UINT16)
                        max_temperature = (self.spin_temperature_max.value(), TYPES.UINT16)
                        min_temperature = (self.spin_temperature_min.value(), TYPES.UINT16)

                        if command == "STEP COLOR & TEMPERATURE":
                            req_cmd['payloads'] = [mood, rate, min_temperature, max_temperature]
                        else:
                            transition_time = (int(self.transit_color.value()), TYPES.UINT16)
                            req_cmd['payloads'] = [mood, rate, transition_time, min_temperature, max_temperature]
                            
                        
                    elif command == "STOP MOVE STEP":
                        req_cmd['payloads'] = None

                    req_cmd['duration'] = self.wait_level.value() if self.wait_level.value() > 0 else config.DEFAULT_DURATION
                    req_cmd['task_kind'] = config.TASK_CMD

                    commands.append(req_cmd)

            elif "level" in group.objectName():  # level
                for i in range(self.count_level.value()):
                    req_cmd = {}
                    value = config.RANGE_FUNC() if group.findChild(
                        QLineEdit).text() == "" else int(group.findChild(QLineEdit).text())
                    req_cmd['cluster'] = LVL_CTRL_CLUSTER
                    req_cmd['command'] = config.LEVEL_COMMAND_LIST[self.level_commands.currentText(
                    )]
                    command = self.level_commands.currentText()
                    if 'MOVE' in command: # 2 payloads
                        if  'TO' in command:
                            req_cmd['payloads'] = [[int(self.lineEdit_brightness.text()), TYPES.UINT8], [int(self.transit_level.value()), TYPES.UINT16]]
                        else:
                            req_cmd['payloads'] = [[int(self.lineEdit_brightness.text()), TYPES.UINT8], [int(self.transit_level.value()), TYPES.UINT16]]
                        
                    elif 'STEP' in command: # 3 payloads
                        if self.comboBox_level_mode.currentText() == "증가":
                            mode = (0x00, TYPES.ENUM8)
                        else:
                            mode = (0x01, TYPES.ENUM8)
                        
                        step_size = (self.spin_step.value(), TYPES.UINT8)
                        transition_time = (int(self.transit_level.value()), TYPES.UINT16)

                        req_cmd['payloads'] = [mode, step_size, transition_time]
                        

                    elif 'STOP' in command: # 0 payloads
                        req_cmd['payloads'] = None


                    req_cmd['duration'] = self.wait_level.value() if self.wait_level.value() > 0 else config.DEFAULT_DURATION
                    req_cmd['task_kind'] = config.TASK_CMD

                    commands.append(req_cmd)

        for command in commands:
            self.list_gen_cmd.addItem(json.dumps(command))

        if not self.btn_test_start.isEnabled() and self.list_gen_cmd.count() > 0:
            self.btn_test_start.setEnabled(True)

    # handling command list - remove only

    def func_cmd_list_double_clicked(self):
        self.list_gen_cmd.takeItem(self.list_gen_cmd.currentRow())

    def func_cmd_reset_clicked(self):
        self.list_gen_cmd.clear()
        if self.btn_test_start.isEnabled():
            self.btn_test_start.setEnabled(False)

    def func_cmd_save_clicked(self):
        commands = []
        for index in range(self.list_gen_cmd.count()):
            commands.append(self.list_gen_cmd.item(index).text())
        json_format = {'tasks': commands}
        import time
        timestr = time.strftime("%Y%m%d-%H%M%S")
        command_file = os.path.join(command_path, timestr + '.json')

        with open(command_file, 'w') as f:
            try:
                f.write(json.dumps(json_format))
                QMessageBox.about(
                    self, "message", command_file + " is created")
            except Exception:
                QMessageBox.about(self, "message", Exception)

    @pyqtSlot(str)
    def thread_func_add_current_result(self, msg):
        # self.list_exec.addItem(msg)
        row = self.table_current_result.rowCount()
        self.table_current_result.setRowCount(row+1)
        result = msg.split('\t')
        for col in range(self.table_current_result.columnCount()):
            print(row, col, result[col])
            self.table_current_result.setItem(row, col, QTableWidgetItem(result[col]))
            self.table_current_result.item(row,col).setForeground(QBrush(QColor(255, 255, 255)))
            if result[-1] == "OK":
                self.table_current_result.item(row,col).setBackground(QColor(0,128,0))
            else:
                self.table_current_result.item(row,col).setBackground(QColor(255,0,0))

    @pyqtSlot(list)
    def thread_func_add_final_result(self,msg_list):
        report = {}
        commands = []
        commands = list(config.ONOFF_COMMAND_LIST.keys()) + list(config.LEVEL_COMMAND_LIST.keys()) + list(config.COLOR_COMMAND_LIST.keys())
        for command in commands:
            report[command] = []

        for msg in msg_list:
            result = msg.split('\t')
            report[result[1]].append(result)   #result[1] = command
        
        for k, v in report.items():
            oks = 0
            ngs = 0
            for result in v:
                if result[-1] == 'OK':
                    oks += 1
                else:
                    ngs += 1

            if len(v) > 0:
                str_result = "명령어: {} \t OK: {} \t NG: {}".format(k, oks, ngs)
                self.list_result.addItem(str_result)
                
    def func_test_start_clicked(self):
        
        self.dict_device['module'] = self.combo_module_select.currentText()
        self.dict_device['name'] = self.text_name.text()
        # dict_device['uuid'] = self.text_uuid.text()
        self.dict_device['eui64'] = int(self.text_address.text(), 16)
        self.dict_device['ep'] = int(self.text_entrypoint.text())

        commands = {}
        commands['tasks'] = []
        for index in range(self.list_gen_cmd.count()):
            commands['tasks'].append(self.list_gen_cmd.item(index).text())

        iter_count = self.entire_iter.value()
        if iter_count < 2:
            iter_count = 1
        current_port = self.combo_port_select.currentText();

        device = Device(self.dict_device['name'], 0,
                        self.dict_device['eui64'], self.dict_device['ep'])
        task_list = parse_task_list(commands)

        
        self.worker = Worker(device, task_list, iter_count, current_port, parent=self)
        self.worker.command_complete.connect(self.thread_func_add_current_result)
        self.worker.test_complete.connect(self.thread_func_add_final_result)
        self.worker.start()


        # log_path = Tester(self.dict_device, commands, current_port, iter_count, self)
        # result_parser.analyze_result(log_path, self)

class Worker(QThread):
    command_complete = pyqtSignal(str)
    test_complete = pyqtSignal(list)

    def __init__(self, device, task_list, iter_count, port, parent=None):
        super().__init__()
        self.main = parent
        self.working = True
        self.device = device
        self.iter_count = iter_count
        self.task_list = task_list
        self.cli_instance = ZbCliDevice('', '', port)

    def run(self):
        while self.working:
            results = []
            for i in range(self.iter_count):
                for task in self.task_list:
                    result = ""
                    if task.task_kind == config.TASK_CMD:
                        attr_list = task.get_dependent_attr_list()
                        previous_attr_list = []
                        for attr_id in attr_list:
                            attr = ReadAttr(task.cluster, attr_id, 0)
                            attr_param = Attribute(attr.cluster, attr.attr_id, attr.attr_type)
                            returned_attr = self.cli_instance.zcl.readattr(self.device.addr, attr_param, ep=self.device.ep)
                            previous_attr_list.append(returned_attr)

                        if len(previous_attr_list) == 1:
                            previous_attr = previous_attr_list[0]
                            previous_value = previous_attr.value


                        if task.payloads == None:
                            self.cli_instance.zcl.generic(
                                eui64=self.device.addr,
                                ep=self.device.ep,
                                profile=constants.DEFAULT_ZIGBEE_PROFILE_ID,
                                cluster=task.cluster,
                                cmd_id=task.command)
                        else:
                            self.cli_instance.zcl.generic(
                                eui64=self.device.addr,
                                ep=self.device.ep,
                                profile=constants.DEFAULT_ZIGBEE_PROFILE_ID,
                                cluster=task.cluster,
                                cmd_id=task.command,
                                payload=task.payloads)

                        time.sleep(task.duration)
                        attr_list = task.get_dependent_attr_list()
                        returned_attr_list = []
                        for attr_id in attr_list:
                            attr = ReadAttr(task.cluster, attr_id, 0)
                            attr_param = Attribute(attr.cluster, attr.attr_id, attr.attr_type)
                            returned_attr = self.cli_instance.zcl.readattr(self.device.addr, attr_param, ep=self.device.ep)
                            returned_attr_list.append(returned_attr)
                            time.sleep(task.duration)

                        
                        if len(returned_attr_list) == 1:
                            returned_attr = returned_attr_list[0]                           

                        if task.cluster is constants.ON_OFF_CLUSTER:
                            cluster = "ON/OFF"
                            cmd = [k for k, v in config.ONOFF_COMMAND_LIST.items() if v == task.command][0]
                            attr_name = returned_attr.name
                            attr_value = returned_attr.value
                            payload = task.payloads
                            transition_time = None
                            wait_time = config.DEFAULT_DURATION

                            if cmd == "ON":
                                expected = True
                                
                            elif cmd == "TOGGLE":
                                if previous_value:
                                    expected = False
                                else:
                                    expected = True
                            else:
                                expected = False

                            if expected == attr_value:
                                okng = "OK"
                            else:
                                okng = "NG"

                            result = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                                cluster, cmd, attr_name, attr_value, payload, transition_time, wait_time, okng)

                        elif task.cluster is constants.LVL_CTRL_CLUSTER:
                            cluster = "LEVEL"
                            cmd = [k for k, v in config.LEVEL_COMMAND_LIST.items() if v == task.command][0]
                            attr_name = returned_attr.name
                            attr_value = returned_attr.value
                            wait_time = task.duration
                            okng = ""
                            if cmd == "MOVE TO":
                                transition_time = task.payloads[1][0]
                                payload = task.payloads[0][0]
                                if attr_value == payload:
                                    okng = "OK"
                                else:
                                    okng = "NG"

                            elif cmd == "STEP" or cmd == "STEP ONOFF":
                                payload = task.payloads[1][0]
                                transition_time = task.payloads[2][0]
                                expected = previous_value + payload if task.payloads[0][0] == 0 else previous_value - payload
                                attr_name = "{}-{}".format("UP", previous_value) if task.payloads[0][0] == 0 else "{}-{}".format("DOWN", previous_value)
                                if attr_value == expected:
                                    okng = "OK"
                                else:
                                    okng = "NG"

                            result = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                                cluster, cmd, attr_name, attr_value, payload, transition_time, wait_time, okng)

                        else:
                        #elif task.cluster is constants.COLOR_CTRL_CLUSTER:
                            cluster = "COLOR"
                            cmd = [k for k, v in config.COLOR_COMMAND_LIST.items() if v == task.command][0]
                            # attr_name = returned_attr.name
                            # attr_value = returned_attr.value
                            wait_time = task.duration
                            
                            # @hipiphock
                            if cmd == "MOVE TO COLOR":
                                attr_name = "{},{}".format("x", "y")
                                payload_x, payload_y = task.payloads[0][0], task.payloads[1][0]
                                transition_time = task.payloads[2][0]
                                payload = "{},{}".format(payload_x, payload_y)
                                attr_value = "{},{}".format(returned_attr_list[0].value, returned_attr_list[1].value)
                                if returned_attr_list[0].value == payload_x and returned_attr_list[1].value == payload_y:
                                    okng = "OK"
                                else:
                                    okng = "NG"
                            elif cmd == "MOVE COLOR":
                                pass
                            elif cmd == "STEP COLOR":
                                # previous value settings
                                attr_name = "{},{}".format("x", "y")
                                prevous_x, previous_y = previous_attr_list[1].value, previous_attr_list[2].value
                                payload_x, payload_y = task.payloads[0][0], task.payloads[1][0]
                                
                                payload = "{},{}".format(payload_x, payload_y)
                                attr_value = "{},{}".format(returned_attr_list[0].value, returned_attr_list[1].value)

                                transition_time = task.payloads[2][0]
                                expected_x, expected_y = previous_x + payload_x, previous_y + payload_y
                                if returned_attr_list[0].value == expected_x and returned_attr_list[1].value == expected_y:
                                    okng = "OK"
                                else:
                                    okng = "NG"
                            elif cmd == "STOP MOVE STEP":
                                attr_name = "{}".format("temperature")
                                payload = task.payloads
                                if returned_attr.value == 0:
                                    okng = "OK"
                            elif cmd == "MOVE TO COLOR & TEMPERATURE":
                                attr_name = "{}".format("temperature")
                                payload = task.payloads[0][0]
                                attr_value = returned_attr_list.value
                                transition_time = task.payloads[1][0]
                                if returned_attr.value == payload:
                                    okng = "OK"
                                else:
                                    okng = "NG"
                            elif cmd == "MOVE COLOR & TEMPERATURE":
                                pass
                            elif cmd == "STEP COLOR & TEMPERATURE":
                                previous_value = previous_attr_list[2].value
                                payload_size = task.payloads[1][0]
                                transition_time = task.payloads[2][0]
                                payload_min_temp = task.payloads[3][0]
                                payload_max_temp = task.payloads[4][0]
                                
                                attr_name = "{},{},{},{}".format("mode", "step", "min", "max")
                                attr_value = "{},{},{}".format(returned_attr_list[2].value, returned_attr_list[3].value, returned_attr_list[4].value)
                                payload = "{},{},{}".format(payload_size, payload_min_temp, payload_max_temp)
                                if returned_attr_list[2].value == payload_size + previous_value and\
                                        returned_attr[3].value == payload_min_temp and\
                                        returned_attr[4].value == payload_max_temp:
                                    okng = "OK"
                                else:
                                    okng = "NG"                      
                            
                            result = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                                cluster, cmd, attr_name, attr_value, payload, transition_time, wait_time, okng)
                            

                    elif task.task_kind == config.TASK_READ:
                        param_attr = Attribute(task.cluster, task.attr_id, task.attr_type)
                        returned_attr = self.cli_instance.zcl.readattr(self.device.addr, param_attr, ep=self.device.ep)
                    
                    self.command_complete.emit(result)
                    results.append(result)
                    time.sleep(config.DEFAULT_DURATION)

            self.cli_instance.close_cli()
            self.working = False
            self.test_complete.emit(results)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
