import unittest
import os
import string
import re
import common
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BeakerPageTest(unittest.TestCase, common.BeakerCommonLib):
    def setUp(self):
        self.prepare_environment()
        self.open_firefox_with_user()
    
    def test_click_system_page(self):
        driver=self.driver
        system_page={'/':'Systems','/available/':'Available Systems','/free/':'Free Systems'}
        for sub_page in system_page:
            driver.find_element_by_xpath("//ul[@class='nav']/li[1]/a[1]").click()
            driver.implicitly_wait(2)
            subpage_xpath="//a[@href='"+sub_page+"']"
            driver.find_element_by_xpath(subpage_xpath).click()
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.title_contains(system_page[sub_page]))
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
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.title_contains("Devices"))
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
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.title_contains(distro_page[sub_page]))
            self.assertIn(distro_page[sub_page],driver.title)
     
    def test_click_scheduler_page(self):
        driver=self.driver
        scheduler_page={'/jobs/new':'New Job','/jobs':'Jobs','/recipes':'Recipes','/tasks/new':'New Task','/tasks':'Task Library','/watchdogs':'Watchdogs','/reserveworkflow':'Reserve Workflow'}
        for sub_page in scheduler_page:
            driver.find_element_by_xpath("//ul[@class='nav']/li[4]/a[1]").click()
            driver.implicitly_wait(2)
            subpage_xpath="//a[@href='"+sub_page+"']"
            driver.find_element_by_xpath(subpage_xpath).click()
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.title_contains(scheduler_page[sub_page]))
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
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.title_contains(reports_page[sub_page]))
            self.assertIn(reports_page[sub_page],driver.title)

    def test_click_activity_page(self):
        driver=self.driver 
        activity_page={'/activity/':'Activity','/activity/system':'System Activity','/activity/labcontroller':'Lab Controller Activity','/activity/group':'Group Activity','/activity/distro':'Distro Activity','/activity/distrotree':'Distro Tree Activity'}
        for sub_page in activity_page:
            driver.find_element_by_xpath("//ul[@class='nav']/li[6]/a[1]").click()
            driver.implicitly_wait(2)
            subpage_xpath="//a[@href='"+sub_page+"']"
            driver.find_element_by_xpath(subpage_xpath).click()
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.title_contains(activity_page[sub_page]))
            self.assertIn(activity_page[sub_page],driver.title)

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
