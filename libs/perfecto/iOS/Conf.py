import unittest
import urllib3
import os
from appium import webdriver
#from selenium import webdriver
from perfecto import PerfectoExecutionContext,TestResultFactory, TestContext, PerfectoReportiumClient, model


class BaseTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        #Suppress InsecureRequestWarning: Unverified HTTPS request is being made 
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        self.securityToken = os.environ['OFFLINE_TOKEN']
        #self.host = os.environ['LAB'] + '.perfectomobile.com'
        self.driver = None
        #self.cloudName = None
        self.reporting_client = None
        super(BaseTest, self).__init__(*args, **kwargs)

    def setUp(self):
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
            
        cloudName = "tip"    
        # Initialize the Appium driver with Perfecto
        self.driver = webdriver.Remote('https://' + cloudName + '.perfectomobile.com/nexperience/perfectomobile/wd/hub', capabilities)
        # set implicit wait time 
        self.driver.implicitly_wait(20)

        #Create Reportium Client
        self.create_reporting_client()
        cf1 = model.CustomField('key1', 'Tvalue1')
        cf2 = model.CustomField('key2', 'Tvalue2')
        self.reporting_client.test_start(self.id(),TestContext(customFields=[cf1, cf2], tags=['Tag1', 'Tag2', 'Tag3']))
 
    def run(self, result=None):
        self.currentResult = result  # remember result for use in tearDown
        unittest.TestCase.run(self, result)  # call superclass run method

    def tearDown(self):
        cf1 = model.CustomField('key1', 'val1')
        cf2 = model.CustomField('key2', 'val2')
        tec = TestContext(customFields=[cf1, cf2], tags=['test1', 'test2'])
        try:
            if self.currentResult.wasSuccessful():self.reporting_client.test_stop(TestResultFactory.create_success())
            else:
                self.reporting_client.test_stop(TestResultFactory.create_failure(self.currentResult.errors,self.currentResult.failures),tec)
            # Print report's url
            print ('Report-Url: ' + self.reporting_client.report_url() + '\n')
        except Exception as e:
            print (e.message)

        try:
            self.driver.close()
        except Exception as e:
            print (e.message)
        finally:
            try:
                self.driver.quit()
            except Exception as e:
                print (e.message)

    def create_reporting_client(self):
        cf1 = model.CustomField('key1','Evalue1')
        cf2 = model.CustomField('key3', 'Evalue3')

        perfecto_execution_context = PerfectoExecutionContext(webdriver=self.driver,
                                                              tags=['Etag0', 'Etag1', 'Etag2', 'Etag3'],
                                                              job=model.Job('JobnameRaj', 12, 'branch_name'),
                                                              project=model.Project('project_name', 2.0),
                                                              customFields=[cf1, cf2])
        
        self.reporting_client = PerfectoReportiumClient(perfecto_execution_context)