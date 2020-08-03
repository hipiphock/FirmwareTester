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

    # handling command interface
    def func_onoff_command_interface(self):
        print(self.onoff_commands.currentText())

    def func_color_command_interface(self):
        print(self.color_commands.currentText())

    def func_level_command_interface(self):
        print(self.level_commands.currentText())

    # command generate
    def func_cmd_gen_clicked(self):
        commands = []
        groups = self.tabWidget.currentWidget().findChildren(QGroupBox)
        for group in groups:
            if "onoff" in group.objectName():  # on/off
                if group.findChild(QSpinBox).objectName() == "count_onoff":
                    # commands are always created as a req/resp pair
                    for i in range(group.findChild(QSpinBox).value()):
                        req_cmd = {}
                        req_cmd['cluster'] = ON_OFF_CLUSTER
                        req_cmd['command'] = config.ONOFF_COMMAND_LIST[self.onoff_commands.currentText(
                        )]
                        req_cmd['payloads'] = None
                        req_cmd['duration'] = config.DEFAULT_DURATION
                        req_cmd['task_kind'] = config.TASK_CMD
                        commands.append(req_cmd)

                        # resp_cmd = {}
                        # resp_cmd['cluster'] = ON_OFF_CLUSTER
                        # resp_cmd['attr_id'] = ON_OFF_ONOFF_ATTR
                        # resp_cmd['duration'] = config.DEFAULT_DURATION
                        # resp_cmd['task_kind'] = config.TASK_READ
                        # commands.append(req_cmd)

                    print(commands)

            elif "color" in group.objectName():  # color
                if group.findChild(QSpinBox).value() > 0 and group.findChild(QSpinBox).objectName() == "count_color":
                    for i in range(group.findChild(QSpinBox).value()):
                        cmd = {}
                        value = config.RANGE_FUNC() if group.findChild(
                            QLineEdit).text() == "" else int(group.findChild(QLineEdit).text())
                        cmd['cluster'] = COLOR_CTRL_CLUSTER
                        cmd['command'] = config.ONOFF_COMMAND_LIST[self.onoff_commands.currentText()]
                        cmd['payloads'] = [[value, '0x21'], [0, '0x21']]
                        commands.append(cmd)

            elif "level" in group.objectName():  # level
                if group.findChild(QSpinBox).value() > 0:
                    for i in range(group.findChild(QSpinBox).value()):
                        cmd = {}
                        value = config.RANGE_FUNC() if group.findChild(
                            QLineEdit).text() == "" else int(group.findChild(QLineEdit).text())
                        cmd['cluster'] = '0x0008'
                        cmd['command'] = '0x04'
                        cmd['payloads'] = [[value, '0x21'], [0, '0x21']]
                        commands.append(cmd)

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
        print(port)
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

                        # read first
                        attr_id, attr_type = get_attr_element(
                            task.cluster, task.command)
                        param_attr = Attribute(task.cluster, attr_id, attr_type)
                        previous_attr = self.cli_instance.zcl.readattr(
                            self.device.addr, param_attr, ep=self.device.ep        
                        )
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
                        attr_id, attr_type = get_attr_element(
                            task.cluster, task.command)
                        param_attr = Attribute(task.cluster, attr_id, attr_type)
                        returned_attr = self.cli_instance.zcl.readattr(
                            self.device.addr, param_attr, ep=self.device.ep)
                        
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
