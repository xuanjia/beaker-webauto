import unittest
import os
import string
import re
import config
import common
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select as WebDriverSelect

class BeakerDistroTest(unittest.TestCase,common.BeakerCommonLib):
    def setUp(self):
        self.open_firefox_with_user()
    
    def get_first_id_from_distro_list(self):
        return self.driver.find_element_by_xpath("//tbody/tr[1]/td[1]/a").text

    def get_first_name_from_distro_list(self):
        return self.driver.find_element_by_xpath("//tbody/tr[1]/td[2]/a").text
     
    def get_first_osmajor_from_distro_list(self):
        return self.driver.find_element_by_xpath("//div/table/tbody/tr[1]/td[3]").text

    def get_first_id_from_distro_trees_list(self):
        return self.driver.find_element_by_xpath("//tbody/tr[1]/td[1]/a").text

    def get_first_name_from_distro_trees_list(self):
        return self.driver.find_element_by_xpath("//tbody/tr[1]/td[2]/a").text

    def get_first_osmajor_from_distro_trees_list(self):
        return self.driver.find_element_by_xpath("//tbody/tr[1]/td[5]").text

    def simple_search(self,name):
        simple_search=self.driver.find_element_by_xpath("//input[@class='search-query']")
        simple_search.send_keys(name)
        simple_search.send_keys(Keys.RETURN)

    def distro_advance_search_process(self,name,osmajor):
        driver=self.driver
        driver.find_element_by_id("showadvancedsearch").click()
        driver.implicitly_wait(4)
        table=WebDriverSelect(driver.find_element_by_id("distrosearch_0_table"))
        table.select_by_value("Name")
        operation=WebDriverSelect(driver.find_element_by_id("distrosearch_0_operation"))
        operation.select_by_value("contains")
        value=driver.find_element_by_id("distrosearch_0_value")
        value.send_keys(name)
        driver.find_element_by_xpath("//a[@id='doclink']").click()
        driver.implicitly_wait(4)
        table=WebDriverSelect(driver.find_element_by_id("distrosearch_1_table"))
        table.select_by_value("OSMajor")
        operation=WebDriverSelect(driver.find_element_by_id("distrosearch_1_operation"))
        operation.select_by_value("contains")
        value=driver.find_element_by_id("distrosearch_1_value")
        value.send_keys(osmajor)
    
    def distro_advance_search(self,name,osmajor):
        self.distro_advance_search_process(name,osmajor)
        self.driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()

    def distro_advance_search_2(self,name,osmajor):
        self.distro_advance_search_process(name,osmajor)
        self.driver.find_element_by_xpath("//tr[@id='distrosearch_1']/td/a[@class='btn']").click()
        self.driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()

    def distro_tree_advance_search_process(self,name,osmajor,arch="",variant=""):
        driver=self.driver
        driver.find_element_by_id("showadvancedsearch").click()
        driver.implicitly_wait(2)
        table=WebDriverSelect(driver.find_element_by_id("search_0_table"))
        table.select_by_value("Name")
        operation=WebDriverSelect(driver.find_element_by_id("search_0_operation"))
        operation.select_by_value("contains")
        value=driver.find_element_by_id("search_0_value")
        value.send_keys(name)
        driver.find_element_by_xpath("//a[@id='doclink']").click()
        driver.implicitly_wait(4)
        table=WebDriverSelect(driver.find_element_by_id("search_1_table"))
        table.select_by_value("OSMajor")
        operation=WebDriverSelect(driver.find_element_by_id("search_1_operation"))
        operation.select_by_value("contains")
        value=driver.find_element_by_id("search_1_value")
        value.send_keys(osmajor)
        i='2';
        if arch != "" :
                print arch
		driver.find_element_by_xpath("//a[@id='doclink']").click()
                driver.implicitly_wait(4)
                table=WebDriverSelect(driver.find_element_by_id("search_"+i+"_table"))
                table.select_by_value("Arch")
                operation=WebDriverSelect(driver.find_element_by_id("search_"+i+"_operation"))
                operation.select_by_value("is")
                value=WebDriverSelect(driver.find_element_by_id("search_"+i+"_value"))
                value.select_by_value("x86_64")
                i='3'
        if variant != "" :
                driver.find_element_by_xpath("//a[@id='doclink']").click()
                driver.implicitly_wait(4)
                table=WebDriverSelect(driver.find_element_by_id("search_"+i+"_table"))
                table.select_by_value("Variant")
                operation=WebDriverSelect(driver.find_element_by_id("search_"+i+"_operation"))
                operation.select_by_value("contains")
                value=driver.find_element_by_id("search_"+i+"_value")
                value.send_keys(variant)
               
    def distro_tree_advance_search(self,name,osmajor,arch="",variant=""):
        self.distro_tree_advance_search_process(name,osmajor,arch,variant)
        self.driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()

    def distro_tree_advance_search_2(self,name,osmajor):
        self.distro_tree_advance_search_process(name,osmajor)
        self.driver.find_element_by_xpath("//tr[@id='search_1']/td/a[@class='btn']").click()
        self.driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()

    def test_distro_list(self):
        self.driver.get(config.hub_url+"distros/")
        id=self.get_first_id_from_distro_list()
        name=self.get_first_name_from_distro_list()
        self.simple_search(name)
        self.assertIn(id,self.driver.page_source)

    def test_distro_tree_list(self):
        self.driver.get(config.hub_url+"distrotrees/")
        id=self.get_first_id_from_distro_trees_list()
        name=self.get_first_name_from_distro_trees_list()
        self.simple_search(name)
        self.assertIn(id,self.driver.page_source)

    def test_distro_family_list(self):
        self.driver.get(config.hub_url+"distrofamily/")
        self.assertIn("RedHatEnterpriseLinux",self.driver.page_source)

    def test_distro_advance_list(self):
        self.driver.get(config.hub_url+"distros/")
        id=self.get_first_id_from_distro_list()
        name=self.get_first_name_from_distro_list()
        osmajor=self.get_first_osmajor_from_distro_list()
        self.distro_advance_search(name,osmajor)
        self.assertIn(id,self.driver.page_source)
        self.driver.get(config.hub_url+"distros/")
        self.distro_advance_search_2(name,osmajor)
        self.assertIn(id,self.driver.page_source)

    def test_distro_tree_advance_list(self):
        self.driver.get(config.hub_url+"distrotrees/")
        id=self.get_first_id_from_distro_trees_list()
        name=self.get_first_name_from_distro_trees_list()
        osmajor=self.get_first_osmajor_from_distro_trees_list()
        self.distro_tree_advance_search(name,osmajor)
        self.assertIn(id,self.driver.page_source)
        self.driver.get(config.hub_url+"distrotrees/")
        self.distro_tree_advance_search_2(name,osmajor)
        self.assertIn(id,self.driver.page_source)
    
    def test_distro_pick_system(self):
        driver=self.driver
        driver.get(config.hub_url+"distrotrees/")
        self.distro_tree_advance_search("RHEL-6.5","RedHatEnterpriseLinux6","x86_64","Server")
        driver.find_element_by_xpath("//tr[1]/td[8]/div/a[1]").click()
        self.assertIn("Reserve Systems",driver.title)
        driver.find_element_by_xpath("//tr[1]/td[8]").click()
        driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        job_id=self.get_jobid_after_submit()
        self.cancel_job(job_id)

    def test_distro_pick_any_system(self):
        driver=self.driver
        driver.get(config.hub_url+"distrotrees/")
        self.distro_tree_advance_search("RHEL-6.5","RedHatEnterpriseLinux6","x86_64","Server")
        driver.find_element_by_xpath("//tr[1]/td[8]/div/a[2]").click()
        self.assertIn("Reserve Any System",driver.title)
        driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        job_id=self.get_jobid_after_submit()
        self.cancel_job(job_id)
    
    def tearDown(self):
        self.driver.close()

#suite = unittest.TestLoader().loadTestsFromTestCase(BeakerDistroTest)
#unittest.TextTestRunner(verbosity=2).run(suite)
if __name__ == '__main__':
    unittest.main()
