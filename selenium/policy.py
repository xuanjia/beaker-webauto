import unittest
import os
import string
import re
import config
import common
import time
import glob
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select as WebDriverSelect

class BeakerGroupPolicyTest(unittest.TestCase, common.):
    def setUp(self):
        self.prepare_environment()
        self.open_firefox_with_user()
        #check the test system is available, if not,make it available.
        
        #check the group is availabe, if not, make it available. 
    
    def test_submit_group_job(self):
        driver=self.driver
        driver.get(config.hub_url+"jobs/new")
        driver.find_element_by_id("jobs_filexml").send_keys(os.getcwd()+"/group-demo.xml")
        driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        driver.find_element_by_xpath("//button[@class='btn btn-primary btn-block']").click()
        #check the new job id
        job_id=self.get_jobid_after_submit()
        self.cancel_job(job_id)
        self.open_job_page(job_id)
        self.assertIn("web-auto", driver.page_source)
    
    def check_group_is_available(self,group):
        
    
    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
