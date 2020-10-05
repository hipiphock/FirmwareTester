import os
import platform
import json
from selenium import webdriver
from bs4 import BeautifulSoup

example_page = os.path.abspath(os.path.join(os.path.dirname(__file__), 'example.html'))

class Crawler():
    def __init__(self, isOnline):
        current_platform = platform.platform().lower()
        print(current_platform)
        if isOnline:
            self.online = True
        else:
            self.online = False
        # find driver path
        if "mac" in current_platform:
            self.driver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'drivers', 'mac', 'chromedriver'))
        elif "windows" in current_platform:
            self.driver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'drivers', 'windows', 'chromedriver'))
        elif "linux" in current_platform:
            pass
        

    def login(self):
        if self.online:
            self.driver = webdriver.Chrome(self.driver_path)    
            self.driver.implicitly_wait(3)
            self.driver.get('https://account.smartthings.com/login?redirect=https%3A%2F%2Fgraph.api.smartthings.com%2F')
            self.driver.find_element_by_xpath('//*[@name="saLoginFrm"]/button').click()

    def crawl(self):
        if self.online: 
            if self.driver is None:
                print("no chrome driver")
                return -1
        try:
            if self.online:
                # self.login()
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            else:
                soup = BeautifulSoup(open(example_page, encoding = 'UTF-8'), 'html.parser')
            channel = 0
            zigbee_id = ""
            ul = soup.find_all('ul')
            # get channel
            for li in ul: 
                # if "Channel" in li.getText():
                li_list = li.getText().split('\n')
                for el in li_list:
                    if "Channel" in el:
                        channel = el.split(':')[1].lstrip()


            # get zigbee id, and the following codes need to be change considering multiple wafers
            thead = soup.find_all('thead')
            id_index = 0

            # for index, th in enumerate(thead[0].find_all('th')):
            #     if th.getText().lower() == "zigbee id":
            #         id_index = index
            
            # table = soup.find_all('tr', {"class": "even"})
            # for index, td in enumerate(table[0].find_all('td')):
            #     if index == id_index:
            #         zigbee_id = td.getText()
            bulb_lists = []
            tbody = soup.find_all('tbody')
            for index, tr in enumerate(tbody[0].find_all('tr')):
                name = None
                for index2, td in enumerate(tr.find_all('td')):
                    if index2 == 1:
                        if td.getText() == "ZigBee White Color Temperature Bulb":
                            name = td.getText()
                    elif index2 == 2 and name:
                        bulb_lists.append("{}:{}".format(name, td.getText()))
            print(bulb_lists)
            return channel, bulb_lists

        except:
            pass

