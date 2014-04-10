import unittest
import os
import string
import re
import time
import common
import glob
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select as WebDriverSelect

class BeakerTasksTest(unittest.TestCase,common.BeakerCommonLib):
    def setUp(self):
	self.prepare_environment()
        self.open_firefox_with_user()
        os.system("sed -i -e s/VERSION=1.*/VERSION=1.0/g ./task/Makefile")
    
    def get_task_rpm_package_path(self,dir):
        file=glob.glob(dir+"/task/*.rpm")
        return file
    
    def task_simple_search(self,task_name):
        simple_search=self.driver.find_element_by_xpath("//input[@class='search-query']")
        simple_search.send_keys(task_name)
        simple_search.send_keys(Keys.RETURN)

    def task_advance_search_process(self,task_name,task_type,task_description):
        driver=self.driver
        driver.find_element_by_id("showadvancedsearch").click()
        driver.implicitly_wait(4)
        table=WebDriverSelect(driver.find_element_by_id("tasksearch_0_table"))
        table.select_by_value("Name")
        operation=WebDriverSelect(driver.find_element_by_id("tasksearch_0_operation"))
        operation.select_by_value("contains")
        value=driver.find_element_by_id("tasksearch_0_value")
        value.send_keys(task_name)
        driver.find_element_by_xpath("//a[@id='doclink']").click()
        table=WebDriverSelect(driver.find_element_by_id("tasksearch_1_table"))
        table.select_by_value("Types")
        operation=WebDriverSelect(driver.find_element_by_id("tasksearch_1_operation"))
        operation.select_by_value("contains")
        value=driver.find_element_by_id("tasksearch_1_value")
        value.send_keys(task_type)
        driver.find_element_by_xpath("//a[@id='doclink']").click()
        table=WebDriverSelect(driver.find_element_by_id("tasksearch_2_table"))
        table.select_by_value("Description")
        operation=WebDriverSelect(driver.find_element_by_id("tasksearch_2_operation"))
        operation.select_by_value("contains")
        value=driver.find_element_by_id("tasksearch_2_value")
        value.send_keys(task_description)

    def task_advance_search(self,task_name,task_type,task_description):
        self.task_advance_search_process(task_name,task_type,task_description)
        self.driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()

    def task_advance_search_2(self,task_name,task_type,task_description):
        self.task_advance_search_process(task_name,task_type,task_description)
        self.driver.find_element_by_xpath("//tr[@id='tasksearch_1']/td/a[@class='btn']").click()
        self.driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()

    def test_task_libray_simple_search(self):
        driver=self.driver
        driver.get(self.hub_url+'tasks/')
        task_name="beaker-client"
        self.task_simple_search(task_name)
        self.assertIn(task_name,driver.find_element_by_xpath("//tr[1]/td[1]/a[contains(@href ,'./')]").text)

    def test_task_libray_advance_search(self):
        driver=self.driver
        driver.get(self.hub_url+'tasks/')
        task_name="beaker-client"
        task_type="Sanity"
        task_description="beaker client testing"
        self.task_advance_search(task_name,task_type,task_description)
        self.assertIn(task_name,driver.find_element_by_xpath("//tr[1]/td[1]/a[contains(@href ,'./')]").text)
        driver.get(self.hub_url+'tasks/')
        self.task_advance_search_2(task_name,task_type,task_description)
        self.assertIn(task_name,driver.find_element_by_xpath("//tr[1]/td[1]/a[contains(@href ,'./')]").text)

    def test_new_task(self):
	driver=self.driver
        driver.get(self.hub_url+"/tasks/new")
        os.system("pushd task;rm -rf *.rpm ;make package >> /dev/null ;popd")
        package_name=''.join(self.get_task_rpm_package_path(os.getcwd()))
        driver.find_element_by_id("task_task_rpm").send_keys(package_name)
        driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        self.assertIn("/CoreOS/task/Sanity/beaker-web-automation Added/Updated",driver.page_source)

    def test_newer_task(self):
        driver=self.driver
        driver.get(self.hub_url+"/tasks/new")
        os.system("pushd task;rm -rf *.rpm ;sed -i -e s/VERSION=1.*/VERSION=1.2/g Makefile;make package >> /dev/null ;popd")
        package_name=''.join(self.get_task_rpm_package_path(os.getcwd()))
        driver.find_element_by_id("task_task_rpm").send_keys(package_name)
        driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        self.assertIn("/CoreOS/task/Sanity/beaker-web-automation Added/Updated",driver.page_source)
    
    def test_old_task(self):
        driver=self.driver
        driver.get(self.hub_url+"/tasks/new")
        os.system("pushd task;rm -rf *.rpm ;sed -i -e s/VERSION=1.*/VERSION=1.1/g Makefile >> /dev/null ;make package;popd")
        package_name=''.join(self.get_task_rpm_package_path(os.getcwd()))
        driver.find_element_by_id("task_task_rpm").send_keys(package_name)
        driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        self.assertIn("/CoreOS/task/Sanity/beaker-web-automation Added/Updated",driver.page_source)

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
