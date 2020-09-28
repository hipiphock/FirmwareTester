'''
    this page is the first page of navigator
    user should select the communication protocol (zigbee ha, ble, ble mesh)
'''


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from utils import common

import navigator.zigbee_page

class Navigator(QWizard):
    def __init__(self):
        super().__init__()
        self.setWizardStyle(self.ModernStyle)
        self.setPage(1, select_module())
        self.setPage(int(common.PageNumber.ZIGBEE_HA), navigator.zigbee_page.ZigBeePage())
        
        self.setWindowTitle("Firmware Tester")
        self.resize(800,600)


class select_module(QWizardPage):
    def __init__(self): # set widget layouts
        super().__init__()
        
        self.radiobutton_zigbee = QRadioButton("ZigBee HA")
        self.radiobutton_ble = QRadioButton("BLE")
        self.radiobutton_ble_mesh = QRadioButton("BLE MESH")
        
        self.label_protocols = QLabel("통신 모듈을 선택 해주세요")


        self.layout = QVBoxLayout()
        
        protocol_layout = QVBoxLayout()
        protocol_button_layout = QVBoxLayout()

        protocol_layout.addWidget(self.label_protocols)
        protocol_button_layout.addWidget(self.radiobutton_zigbee)
        protocol_button_layout.addWidget(self.radiobutton_ble)
        protocol_button_layout.addWidget(self.radiobutton_ble_mesh)

        protocol_layout.addLayout(protocol_button_layout)

        self.layout.addLayout(protocol_layout)
        self.setLayout(self.layout)

        self.radiobutton_zigbee.clicked.connect(self.radioButtonClicked)

    def initializePage(self): # initialize widgets
        self.label_protocols.setFont(QFont("Arials", weight=QFont.Bold))
        self.radiobutton_ble.setEnabled(False)
        self.radiobutton_ble_mesh.setEnabled(False)
    
    def radioButtonClicked(self):
        self.clearLayout(self.layout)
        if self.radiobutton_zigbee.isChecked():
            pass
        else:
            pass

    def clearLayout(self, layout):
        print("clear layout")