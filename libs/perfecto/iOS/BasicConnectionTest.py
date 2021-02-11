import time

#from selenium import webdriver
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from perfecto import TestResultFactory
from perfecto import PerfectoExecutionContext,TestResultFactory,TestContext,PerfectoReportiumClient,model
from Conf import BaseTest

capabilities = {
    #  2. Replace <<security token>> with your perfecto security token.
    'securityToken' : "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJqdGkiOiJjYjRjYjQzYi05Y2FiLTQxNzQtOTYxYi04MDEwNTZkNDM2MzgiLCJleHAiOjAsIm5iZiI6MCwiaWF0IjoxNjExNTk0NzcxLCJpc3MiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwiYXVkIjoiaHR0cHM6Ly9hdXRoMi5wZXJmZWN0b21vYmlsZS5jb20vYXV0aC9yZWFsbXMvdGlwLXBlcmZlY3RvbW9iaWxlLWNvbSIsInN1YiI6IjdiNTMwYWUwLTg4MTgtNDdiOS04M2YzLTdmYTBmYjBkZGI0ZSIsInR5cCI6Ik9mZmxpbmUiLCJhenAiOiJvZmZsaW5lLXRva2VuLWdlbmVyYXRvciIsIm5vbmNlIjoiZTRmOTY4NjYtZTE3NS00YzM2LWEyODMtZTQwMmI3M2U5NzhlIiwiYXV0aF90aW1lIjowLCJzZXNzaW9uX3N0YXRlIjoiYWNkNTQ3MTctNzJhZC00MGU3LWI0ZDctZjlkMTAyNDRkNWZlIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZXBvcnRpdW0iOnsicm9sZXMiOlsiYWRtaW5pc3RyYXRvciJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.SOL-wlZiQ4BoLLfaeIW8QoxJ6xzrgxBjwSiSzkLBPYw",
    
    # 3. Set device capabilities.
    'platformName': 'iOS',
    'manufacturer': 'Apple',
    'model': 'iPhone.*',
    
     # 4. Set Perfecto Media repository path of App under test.
    #'app': 'PUBLIC:Genesis/Sample/iOSInvoiceApp1.0.ipa',
    
    # 5. Set the unique identifier of your app
    'bundleId': 'net.techet.netanalyzerlite',
    
    # Set other capabilities.
    'enableAppiumBehavior': True, # Enable new architecture of Appium
    'autoLaunch': True, # To work with hybrid applications, install the iOS/Android application as instrumented.
    'autoInstrument': True, # To work with hybrid applications, install the iOS/Android application as instrumented.
    # 'fullReset': false, # Whether to install and launch the app automatically.
}
# Initialize the Appium driver with Perfecto
driver = webdriver.Remote('https://' + cloudName + '.perfectomobile.com/nexperience/perfectomobile/wd/hub', capabilities)
# set implicit wait time 
driver.implicitly_wait(20)

print("\n-------------------------------------------")
DefaultGateWayAccessPoint = driver.find_element_by_xpath("//*[@label='Default Gateway IP']/parent::*/XCUIElementTypeButton").text
print("Device-DefaultGateWay-AP: " + "'"+ DefaultGateWayAccessPoint + "'")

networkAccessPoint = driver.find_element_by_xpath("//*[@label='Network Connected']/parent::*/XCUIElementTypeButton").text
print("Network-AccessPoint-Connected: " + "'"+ networkAccessPoint + "'")

#Open Setting Application 
params = {'identifier': 'com.apple.Preferences'}
driver.execute_script('mobile:application:open', params)

#Verify Wifi Connected Network
element = driver.find_element_by_xpath("//XCUIElementTypeCell[@name='Wi-Fi']/XCUIElementTypeStaticText[2]")
Wifi_AP_Name = element.text
print("Wifi_AP_ConnName: " + "'"+ Wifi_AP_Name + "'")

#Verify if Ap is connected with Wifi
element.click()
WifiXpath = "//*[@label='selected']/parent::*/parent::*/XCUIElementTypeStaticText[@label='"+ Wifi_AP_Name + "']"
element = driver.find_element_by_xpath(WifiXpath)
print("Connected-Wifi-AP: " + "'"+ element.text + "'" + "....Connection Successfull")    

#Close Settings App
driver.execute_script('mobile:application:close', params)

#Open Ping App
params2 = {'identifier': 'com.deftapps.ping'}
driver.execute_script('mobile:application:open', params2)

pingHost = "//*[@value='<Hostname or IP address>']"
element2 = driver.find_element_by_xpath(pingHost)
element2.clear()
element2.send_keys(DefaultGateWayAccessPoint)

#Ping Enable
element3 = driver.find_element_by_xpath("//XCUIElementTypeButton[@label='Ping']")
#element3.click()

time.sleep(10)

#element4 = driver.find_element_by_xpath("//*[@label='Stop']")
#element4.click()

#Close Settings App
driver.execute_script('mobile:application:close', params2)

#Quits the driver
#driver.close()
driver.close_app()
driver.quit()
print("\n-------------------------------------------")