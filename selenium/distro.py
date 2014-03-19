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
from selenium.webdriver.support.select import Select as WebDriverSelect

class BeakerDistroTest(unittest.TestCase):
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

    def distro_tree_advance_search_process(self,name,osmajor):
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
    
    def distro_tree_advance_search(self,name,osmajor):
        self.distro_tree_advance_search_process(name,osmajor)
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

    def tearDown(self):
        self.driver.close()

#suite = unittest.TestLoader().loadTestsFromTestCase(BeakerDistroTest)
#unittest.TextTestRunner(verbosity=2).run(suite)
if __name__ == '__main__':
    unittest.main()
