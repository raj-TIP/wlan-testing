import time

from selenium import webdriver
#from appium import webdriver


 #  1. Replace <<cloud name>> with your perfecto cloud name (e.g. demo is the cloudName of demo.perfectomobile.com).
cloudName = "tip"

capabilities = {
    #  2. Replace <<security token>> with your perfecto security token.
    'securityToken' : "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJqdGkiOiJjYjRjYjQzYi05Y2FiLTQxNzQtOTYxYi04MDEwNTZkNDM2MzgiLCJleHAiOjAsIm5iZiI6MCwiaWF0IjoxNjExNTk0NzcxLCJpc3MiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwiYXVkIjoiaHR0cHM6Ly9hdXRoMi5wZXJmZWN0b21vYmlsZS5jb20vYXV0aC9yZWFsbXMvdGlwLXBlcmZlY3RvbW9iaWxlLWNvbSIsInN1YiI6IjdiNTMwYWUwLTg4MTgtNDdiOS04M2YzLTdmYTBmYjBkZGI0ZSIsInR5cCI6Ik9mZmxpbmUiLCJhenAiOiJvZmZsaW5lLXRva2VuLWdlbmVyYXRvciIsIm5vbmNlIjoiZTRmOTY4NjYtZTE3NS00YzM2LWEyODMtZTQwMmI3M2U5NzhlIiwiYXV0aF90aW1lIjowLCJzZXNzaW9uX3N0YXRlIjoiYWNkNTQ3MTctNzJhZC00MGU3LWI0ZDctZjlkMTAyNDRkNWZlIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZXBvcnRpdW0iOnsicm9sZXMiOlsiYWRtaW5pc3RyYXRvciJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.SOL-wlZiQ4BoLLfaeIW8QoxJ6xzrgxBjwSiSzkLBPYw",
    
    # 3. Set device capabilities.
    'platformName': 'Android',
    
     # 4. Set Perfecto Media repository path of App under test.
    #'app': 'PUBLIC:ExpenseTracker/Native/ExpenseAppVer1.0.apk',
    
    # 5. Set the unique identifier of your app
    'bundleId': 'net.techet.netanalyzerlite',
    #'deviceSessionId' : '80796CEF0DE687CB0609FA9AD002FB5C',

    # Set other capabilities.
    'enableAppiumBehavior': True, # Enable new architecture of Appium
    'autoLaunch': True, # Whether to have Appium install and launch the app automatically.
    'autoInstrument': True, # To work with hybrid applications, install the iOS/Android application as instrumented.
    # 'fullReset': false, # Whether to install and launch the app automatically.

   
}
# Initialize the Appium driver
driver = webdriver.Remote('https://' + cloudName + '.perfectomobile.com/nexperience/perfectomobile/wd/hub', capabilities)
# set implicit wait time 
driver.implicitly_wait(15)


#to get ip address AP
#net.techet.netanalyzerlite

#Verify Wifi information
    #

#Ping App  com.deftapps.ping

#Youtube appcom.google.ios.youtube


# Your code goes here
time.sleep(5)

#Quits the driver
driver.close()
driver.quit()
print("Python Android Execution completed")