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
    
    def test_click_system_page(self):
        driver=self.driver
        system_page={'/':'Systems','/available/':'Available Systems','/free/':'Free Systems'}
        for sub_page in system_page:
            driver.find_element_by_xpath("//ul[@class='nav']/li[1]/a[1]").click()
            driver.implicitly_wait(2)
            subpage_xpath="//a[@href='"+sub_page+"']"
            driver.find_element_by_xpath(subpage_xpath).click()
            self.assertIn(system_page[sub_page],driver.title)
     
    def test_click_devices_page(self):
        driver=self.driver
        driver.find_element_by_xpath("//ul[@class='nav']/li[2]/a[1]").click()
        driver.implicitly_wait(2)
        driver.find_element_by_xpath("//a[@href='/devices']").click()
        self.assertIn("Devices",driver.title)
        for sub_page in ['None','NETWORK','OTHER','MOUSE','IDE','KEYBOARD','USB','VIDEO','RAID','SCSI','FIREWIRE','AUDIO']:
            driver.find_element_by_xpath("//ul[@class='nav']/li[2]/a[1]").click()
            driver.implicitly_wait(2)
            subpage_xpath="//a[@href='/devices/"+sub_page+"']"
            driver.find_element_by_xpath(subpage_xpath).click()
            self.assertIn("Devices",driver.title)
            self.assertIn(sub_page,driver.page_source)
    
    def test_click_distros_page(self):
        driver=self.driver
        distro_page={'/distros':'Distros','/distrotrees/':'Distro Trees','/distrofamily':'OS Versions'}
        for sub_page in distro_page:
            driver.find_element_by_xpath("//ul[@class='nav']/li[3]/a[1]").click()
            driver.implicitly_wait(2)
            subpage_xpath="//a[@href='"+sub_page+"']"
            driver.find_element_by_xpath(subpage_xpath).click()
            self.assertIn(distro_page[sub_page],driver.title)
     
    def test_click_scheduler_page(self):
        driver=self.driver
        scheduler_page={'/jobs/new':'New Job','/jobs':'Jobs','/recipes':'Recipes','/tasks/new':'New Task','/tasks':'Task Library','/watchdogs':'Watchdogs','/reserveworkflow':'Reserve Workflow'}
        for sub_page in scheduler_page:
            driver.find_element_by_xpath("//ul[@class='nav']/li[4]/a[1]").click()
            driver.implicitly_wait(2)
            subpage_xpath="//a[@href='"+sub_page+"']"
            driver.find_element_by_xpath(subpage_xpath).click()
            self.assertIn(scheduler_page[sub_page],driver.title)

    def test_click_reports_page(self):
        driver=self.driver
        driver.find_element_by_xpath("//a[@href='/login']").click()
        reports_page={'/reports':'Reserve Report','/matrix':'Job Matrix Report','/csv':'CSV Export','/tasks/executed':'Executed Tasks','/reports/external':'External Reports','/reports/partner_hardware/':'Partner Hardware Report'}
        for sub_page in reports_page:
            driver.find_element_by_xpath("//ul[@class='nav']/li[5]/a[1]").click()
            driver.implicitly_wait(2)
            subpage_xpath="//a[@href='"+sub_page+"']"
            driver.find_element_by_xpath(subpage_xpath).click()
            self.assertIn(reports_page[sub_page],driver.title)

    def test_click_activity_page(self):
        driver=self.driver 
        activity_page={'/activity/':'Activity','/activity/system':'System Activity','/activity/labcontroller':'Lab Controller Activity','/activity/group':'Group Activity','/activity/distro':'Distro Activity','/activity/distrotree':'Distro Tree Activity'}
        for sub_page in activity_page:
            driver.find_element_by_xpath("//ul[@class='nav']/li[6]/a[1]").click()
            driver.implicitly_wait(2)
            subpage_xpath="//a[@href='"+sub_page+"']"
            driver.find_element_by_xpath(subpage_xpath).click()
            self.assertIn(activity_page[sub_page],driver.title)

    def tearDown(self):
        self.driver.close()

suite = unittest.TestLoader().loadTestsFromTestCase(BeakerPageTest)
unittest.TextTestRunner(verbosity=2).run(suite)

