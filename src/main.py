import os
import sys
import json

import serial
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from WebCrawler import crawler
from Handler.Zigbee.constants import *
from CommandGenerator.command_generator import CmdGenerator

ui_file = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'ui', 'new_main.ui'))

main_class = uic.loadUiType(ui_file)[0]

def get_enable_ports():
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


class WindowClass(QMainWindow, main_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.crawler = crawler.Crawler()
    
        self.set_enable_ports()
        self.pushButton_zigbee_webcrwal.clicked.connect(self.func_btn_zigbee_crwaler)
        self.comboBox_level_commands.currentIndexChanged.connect(self.func_level_interface)
        self.comboBox_color_commands.currentIndexChanged.connect(self.func_color_interface)
        self.pushButton_cmd_gen.clicked.connect(self.func_btn_command_generator)
        self.list_gen_cmd.itemDoubleClicked.connect(self.func_cmd_list_double_clicked)
        self.init_commands()
        self.cmd_generator = CmdGenerator()


    def init_commands(self):
        try:
            # init level commands
            level_commands = list(commands['LEVEL'].keys())
            for command in level_commands:
                self.comboBox_level_commands.addItem(command)

            color_commands = list(commands['COLOR'].keys())
            for command in color_commands:
                self.comboBox_color_commands.addItem(command)

            self.groupBox_cmd_gen.setEnabled(False) # disable all commands
        except:
            pass
    
    def set_cmd_gen_enable(self):
        self.groupBox_cmd_gen.setEnabled(True)

    def set_enable_ports(self):
        enabled_ports = get_enable_ports()
        
        for port in enabled_ports:
            self.comboBox_port.addItem(port)


    def func_btn_command_generator(self):
        commands = []
        
        try:
        # connection
            connection_enabled = self.checkBox_connection.isChecked()
            commands.append(self.cmd_generator.cmd_connect(channel=self.lineEdit_zigbee_channel.text(), port = self.comboBox_port.currentText() ,enabled=connection_enabled))       

            # on/off
            for i in range(self.spinBox_count_onoff.value()):
                commands.append(self.cmd_generator.cmd_onoff(on=self.radioButton_on.isChecked(), off=self.radioButton_off.isChecked(), toggle=self.radioButton_toggle.isChecked()))

            # level
            for i in range(self.spinBox_count_level.value()):
                for child in self.vlayout_level_widget.children():
                    pass
                    
            # color
            for i in range(self.spinBox_count_color.value()):
                pass

            # show commands 
            for i in range(self.spinBox_iter_entire.value()):
                for command in commands:
                    self.list_gen_cmd.addItem(json.dumps(command))

        except Exception:
            print(str(Exception))
        
        finally:
            self.func_level_interface()

    def func_cmd_list_double_clicked(self):
        self.list_gen_cmd.takeItem(self.list_gen_cmd.currentRow())


    def func_btn_zigbee_crwaler(self):
        try:
            channel, zigbee_id = self.crawler.crawl()
            self.lineEdit_zigbee_channel.setText(channel)
            self.lineEdit_zigbee_id.setText(zigbee_id) # this should be changed as combobox later
            self.set_cmd_gen_enable()
        except:
            pass # put error messages here

    def func_level_interface(self):
        try:
            current_cmd = self.comboBox_level_commands.currentText()
            self.clear_layout(self.vlayout_level_widget)

            if commands['LEVEL'][current_cmd] == LVL_CTRL_MV_TO_LVL_CMD or commands['LEVEL'][current_cmd] == LVL_CTRL_MV_TO_LVL_ONOFF_CMD:
                hlayout_brightness = QHBoxLayout()
                label_brightness = QLabel("밝기")
                spinbox_brightness = QSpinBox()
                spinbox_brightness.setMaximum(254) # 254 should be changed as constants.maxvalue
                hlayout_brightness.addWidget(label_brightness)
                hlayout_brightness.addWidget(spinbox_brightness)
                
                hlayout_random = self.func_layout_random()
                hlayout_transition, hlayout_wait = self.func_layout_transition_time()

                self.put_layout(self.vlayout_level_widget, hlayout_brightness, hlayout_random, hlayout_transition, hlayout_wait)
                
            elif commands['LEVEL'][current_cmd] == LVL_CTRL_MOVE_CMD or commands['LEVEL'][current_cmd] == LVL_CTRL_MOVE_ONOFF_CMD:
                hlayout_minmax = QHBoxLayout()
                label_minmax = QLabel("최대/최소")
                combobox_minmax = QComboBox()
                combobox_minmax.addItem("최대")
                combobox_minmax.addItem("최소")
                hlayout_minmax.addWidget(label_minmax)
                hlayout_minmax.addWidget(combobox_minmax)

                self.put_layout(self.vlayout_level_widget, hlayout_minmax)

            elif commands['LEVEL'][current_cmd] == LVL_CTRL_STEP_CMD or commands['LEVEL'][current_cmd] == LVL_CTRL_STEP_ONOFF_CMD:
                pass

            elif commands['LEVEL'][current_cmd] == LVL_CTRL_STOP_CMD or commands['LEVEL'][current_cmd] == LVL_CTRL_STOP_ONOFF_CMD:
                self.clear_layout(self.vlayout_level_widget)


        except Exception:
           print(Exception) # put error messages here
    
    def func_layout_random(self):
        hlayout_random = QHBoxLayout()
        label_random = QLabel("임의값")
        radio_normal = QRadioButton("정상 범위")
        radio_abnormal = QRadioButton("비정상 범위")
        hlayout_random.addWidget(label_random)
        hlayout_random.addWidget(radio_normal)        
        hlayout_random.addWidget(radio_abnormal)

        return hlayout_random

    

    def func_color_interface(self):
        try:
            current_cmd = self.comboBox_color_commands.currentText()
            self.clear_layout(self.vlayout_color_widget)

            if commands['COLOR'][current_cmd] == COLOR_CTRL_MV_TO_COLOR_TEMP_CMD:
                hlayout_mired = QHBoxLayout()
                label_mired = QLabel("온도(Mired)")
                spinbox_mired = QSpinBox()
                spinbox_mired.setMinimum(200)
                spinbox_mired.setMaximum(370)

                hlayout_mired.addWidget(label_mired)
                hlayout_mired.addWidget(spinbox_mired)

                hlayout_random = self.func_layout_random()
                hlayout_transtition, hlayout_wait = self.func_layout_transition_time()

                self.put_layout(self.vlayout_color_widget, hlayout_mired, hlayout_random, hlayout_transtition, hlayout_wait)
            
            elif commands['COLOR'][current_cmd] == COLOR_CTRL_MV_TO_COLOR_CMD:
                hlayout_color_x = QHBoxLayout()
                label_color_x = QLabel("Color X (hex)")
                lineEdit_color_x = QLineEdit()
                hlayout_color_x.addWidget(label_color_x)
                hlayout_color_x.addWidget(lineEdit_color_x)

                hlayout_color_y = QHBoxLayout()
                label_color_y = QLabel("Color Y (hex)")
                lineEdit_color_y = QLineEdit()
                hlayout_color_y.addWidget(label_color_y)
                hlayout_color_y.addWidget(lineEdit_color_y)

                hlayout_random = self.func_layout_random()
                hlayout_transtition, hlayout_wait = self.func_layout_transition_time()
                
                self.put_layout(self.vlayout_color_widget, hlayout_color_x, hlayout_color_y, hlayout_random, hlayout_transtition, hlayout_wait)

        except:
            pass

    def func_layout_transition_time(self):
        hlayout_transition = QHBoxLayout()
        label_transition = QLabel("전환시간(ms)")
        spinbox_transition = QSpinBox()
        spinbox_transition.setMinimum(500)
        spinbox_transition.setMaximum(65534)
        hlayout_transition.addWidget(label_transition) 
        hlayout_transition.addWidget(spinbox_transition)

        hlayout_wait = QHBoxLayout()
        label_wait = QLabel("대기시간(ms)")
        spinbox_wait = QSpinBox()
        spinbox_wait.setMinimum(501)
        spinbox_wait.setMaximum(65534)
        hlayout_wait.addWidget(label_wait) 
        hlayout_wait.addWidget(spinbox_wait)

        return hlayout_transition, hlayout_wait

    def func_calculate_wait_time(self, spinbox_wait):
        spinbox_wait.setMinimum(self.spinbox_transition.value() + 1)
        spinbox_wait.setValue(max(self.spinbox_transition.value() + 1, spinbox_wait.value()))

    def clear_layout(self, layout):
        #if type(layout) == QVBoxLayout:
        while layout.count():
            child = layout.takeAt(0)
            if type(child) == QWidgetItem:
                child.widget().deleteLater()
            elif type(child) == QHBoxLayout or type(child) == QVBoxLayout:
                self.clear_layout(child)

    def put_layout(self, parent, *childs):
        for child in childs:
            parent.addLayout(child) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()


