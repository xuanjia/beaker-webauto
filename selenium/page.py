import unittest
import os
import string
import re
import config
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BeakerPageTest(unittest.TestCase):
    def setUp(self):
        profile = webdriver.FirefoxProfile(config.user_noadmin)
        profile.set_preference("browser.download.folderList",2)
        profile.set_preference("browser.download.manager.showWhenStarting",False)
        profile.set_preference("browser.download.dir", os.getcwd()+"/download")
        #set auto download xml file
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/xml")
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
        self.driver = webdriver.Firefox(profile)
        driver = self.driver
        driver.get(config.hub_url)
        self.assertIn("Systems",driver.title)
    
    @staticmethod
    def get_jobid_from_string(job_string):
        p=re.compile(r':')
        job_id=p.split(job_string)[1]
        return job_id

    @staticmethod
    def check_string_in_file(file,string):
        r=open(file)
        found = False
        for line in r:
            if string in line:
                found = True
                break
        return found

    def test_click_avaliable_system(self):
        driver=self.driver
        driver.find_element_by_xpath("//ul[@class='nav']/li[1]/a[1]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//a[@href='/available/']").click()
        time.sleep(2)
        self.assertIn("Available Systems",driver.title)

    def tearDown(self):
        pass
        #self.driver.close()

suite = unittest.TestLoader().loadTestsFromTestCase(BeakerPageTest)
unittest.TextTestRunner(verbosity=2).run(suite)

