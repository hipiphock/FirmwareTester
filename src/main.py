import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from WebCrawler import crawler
from Handler.Zigbee.constants import *

ui_file = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'ui', 'new_main.ui'))

main_class = uic.loadUiType(ui_file)[0]

class WindowClass(QMainWindow, main_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.crawler = crawler.Crawler()
    
        self.pushButton_zigbee_webcrwal.clicked.connect(self.func_btn_zigbee_crwaler)
        self.comboBox_level_commands.currentIndexChanged.connect(self.func_level_interface)
        self.init_commands()

    def init_commands(self):
        try:
            # init level commands
            level_commands = list(commands['LEVEL'].keys())
            for command in level_commands:
                self.comboBox_level_commands.addItem(command)

            color_commands = list(commands['COLOR'].keys())
            for command in color_commands:
                self.comboBox_color_commands.addItem(command)

        except:
            pass

    def func_btn_zigbee_crwaler(self):
        try:
            channel, zigbee_id = self.crawler.crawl()
            self.lineEdit_zigbee_channel.setText(channel)
            self.lineEdit_zigbee_id.setText(zigbee_id) # this should be changed as combobox later
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
                
                # hlayout_random = QHBoxLayout
                self.put_layout(self.vlayout_level_widget, hlayout_brightness)
                
            elif commands['LEVEL'][current_cmd] == LVL_CTRL_MOVE_CMD or commands['LEVEL'][current_cmd] == LVL_CTRL_MOVE_ONOFF_CMD:
                self.clear_layout(self.vlayout_level_widget)

            elif commands['LEVEL'][current_cmd] == LVL_CTRL_STEP_CMD or commands['LEVEL'][current_cmd] == LVL_CTRL_STEP_ONOFF_CMD:
                pass
            elif commands['LEVEL'][current_cmd] == LVL_CTRL_STOP_CMD or commands['LEVEL'][current_cmd] == LVL_CTRL_STOP_ONOFF_CMD:
                pass

        except:
            pass # put error messages here
    
    def clear_layout(self, layout):
        if type(layout) == QVBoxLayout:
            layout.deleteLater()
            # children = layout.children()
            # for child in children:
            #     print(child)
            #     if type(child) == QHBoxLayout:
            #         for widget in child.children():
            #             print(widget)
            #             child.removeWidget(widget)
            #     child.deleteLater()

    def put_layout(self, parent, *childs):
        for child in childs:
            parent.addLayout(child) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()


