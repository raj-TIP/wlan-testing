
from selenium.common.exceptions import NoSuchElementException
#from perfecto import TestResultFactory

import unittest
import time
from selenium.webdriver.common.by import By
from Conf import BaseTest
#libs/perfecto/iOS/Conf.py
class BasicConnectionTestCase(BaseTest):

    def test_navigation(self):
        try:
           # assert 'Perfecto' in self.driver.title
            print("\n-------------------------------------------")
             #REPORTIUM TEST START
            self.reporting_client.step_start("BasicConnectionTest") 
            DefaultGateWayAccessPoint = self.driver.find_element_by_xpath("//*[@label='Default Gateway IP']/parent::*/XCUIElementTypeButton").text
            print("Device-DefaultGateWay-AP: " + "'"+ DefaultGateWayAccessPoint + "'")

            networkAccessPoint = self.driver.find_element_by_xpath("//*[@label='Network Connected']/parent::*/XCUIElementTypeButton").text
            print("Network-AccessPoint-Connected: " + "'"+ networkAccessPoint + "'")

            #Open Setting Application 
            params = {'identifier': 'com.apple.Preferences'}
            self.driver.execute_script('mobile:application:open', params)

            #Verify Wifi Connected Network
            element = self.driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")
            Wifi_AP_Name = element.text
            print("Wifi_AP_ConnName: " + "'"+ Wifi_AP_Name + "'")

            #Verify if Ap is connected with Wifi
            element.click()
            WifiXpath = "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeStaticText[@label='"+ Wifi_AP_Name + "']"
            element = self.driver.find_element_by_xpath(WifiXpath)
            print("Connected-Wifi-AP: " + "'"+ element.text + "'" + "....Connection Successfull")    

            #Close Settings App
            self.driver.execute_script('mobile:application:close', params)

            #Open Ping App
            params2 = {'identifier': 'com.deftapps.ping'}
            self.driver.execute_script('mobile:application:open', params2)

            pingHost = "//*[@value='<Hostname or IP address>']"
            element2 = self.driver.find_element_by_xpath(pingHost)
            element2.clear()
            element2.send_keys(DefaultGateWayAccessPoint)

            #Ping Enable
            element3 = self.driver.find_element_by_xpath("//XCUIElementTypeButton[@label='Ping']")
            #element3.click()

            time.sleep(10)

            #element4 = driver.find_element_by_xpath("//*[@label='Stop']")
            #element4.click()

            #Close Settings App
            self.driver.execute_script('mobile:application:close', params2)
            
            #REPORTIUM TEST END
            self.reporting_client.step_end()

        except NoSuchElementException as ex:
            self.currentResult = False
            #self.reporting_client.test_stop(TestResultFactory.create_failure("NoSuchElementException", ex))
           # print ex
        self.currentResult = True
        #self.reporting_client.test_stop(TestResultFactory.create_success())


if __name__ == '__main__':
    unittest.main()