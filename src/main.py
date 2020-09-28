import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from WebCrawler import crawler
from Handler.Zigbee import constants

ui_file = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'ui', 'new_main.ui'))

main_class = uic.loadUiType(ui_file)[0]

class WindowClass(QMainWindow, main_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.crawler = crawler.Crawler()
    
        self.pushButton_zigbee_webcrwal.clicked.connect(self.func_btn_zigbee_crwaler)
        

    def func_btn_zigbee_crwaler(self):
        try:
            channel, zigbee_id = self.crawler.crawl()
            self.lineEdit_zigbee_channel.setText(channel)
            self.lineEdit_zigbee_id.setText(zigbee_id) # this should be changed as combobox later
        except:
            pass # put error messages here

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()


