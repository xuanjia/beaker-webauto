import unittest
import os
import string
import re
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

class BeakerGroupPolicyTest(unittest.TestCase, common.BeakerCommonLib):
    def setUp(self):
        self.prepare_environment()
        self.open_firefox_with_user()
    
    def test_submit_group_job(self):
        driver=self.driver
        driver.get(self.hub_url+"jobs/new")
        driver.find_element_by_id("jobs_filexml").send_keys(os.getcwd()+"/group-demo.xml")
        driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        driver.find_element_by_xpath("//button[@class='btn btn-primary btn-block']").click()
        #check the new job id
        job_id=self.get_jobid_after_submit()
        self.cancel_job(job_id)
        self.open_job_page(job_id)
        self.assertIn("web-auto", driver.page_source)
    
    def test_delegate_submit_job(self):
        driver=self.driver
        driver.get(self.hub_url+"prefs/")
        delegate_element=driver.find_element_by_id("SubmissionDelegates_user_text")
        delegate_element.send_keys(self.username_2_noadmin)
        delegate_element.send_keys(Keys.RETURN)
        self.driver.close()
        self.open_firefox_with_user_2()
        job_id=self.submit_job(user=self.username_1_noadmin)
        self.cancel_job(job_id)
        #check job list by user2
        self.assertTrue(self.find_job_in_mine_job_list(job_id))
        self.driver.close()
        #check job list by user1
        self.open_firefox_with_user()
        self.assertTrue(self.find_job_in_mine_job_list(job_id))
    
    def test_delegate_submit_group_job(self):
        driver=self.driver
        driver.get(self.hub_url+"prefs/")
        delegate_element=driver.find_element_by_id("SubmissionDelegates_user_text")
        delegate_element.send_keys(self.username_2_noadmin)
        delegate_element.send_keys(Keys.RETURN)
        self.driver.close()
        self.open_firefox_with_user_2()
        job_id=self.submit_job(user=self.username_1_noadmin,group=self.group_name)
        self.cancel_job(job_id)
        #check job list by user2
        #self.assertFalse(self.find_job_in_mine_group_job_list(job_id))
        self.assertTrue(self.find_job_in_mine_group_job_list(job_id))
        self.driver.close()
        #check job list by user1
        self.open_firefox_with_user()
        self.assertTrue(self.find_job_in_mine_group_job_list(job_id))

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
