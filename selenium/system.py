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

class BeakerSystemTest(unittest.TestCase):
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
     
    def get_first_fqdn_from_system_list(self):
        return self.driver.find_element_by_xpath("//tbody/tr[1]/td[1]/a[1]").text

    def get_first_arch_from_system_list(self):
        arch_list=self.driver.find_element_by_xpath("//div/table/tbody/tr[1]/td[5]").text
        p=re.compile(r',')
        return p.split(arch_list)[0]

    def get_first_status_from_system_list(self):
        return self.driver.find_element_by_xpath("//div/table/tbody/tr[1]/td[2]").text

    def get_first_free_system_information(self):
        driver=self.driver
        driver.get(config.hub_url+"/free/")
        fqdn=self.get_first_fqdn_from_system_list()
        arch=self.get_first_arch_from_system_list()
        status=self.get_first_status_from_system_list()
        return fqdn,arch,status

    def is_xpath_present(self,xpath):
        try: self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException, e: return False
        return True
    
    def is_system_in_search_result(self,fqdn):
        xpath="//a[@href='/view/"+fqdn+"']"
        self.assertTrue(self.is_xpath_present(xpath))
    
    def is_type_in_search_result(self,type):
        elements=self.driver.find_elements_by_xpath("//th")
        found=False
        for i,element in enumerate(elements):
            if type == element.text:
                found=True
                break
        self.assertTrue(found)

    def simple_search(self,fqdn):
        simple_search=self.driver.find_element_by_xpath("//input[@class='search-query']")
        simple_search.send_keys(fqdn)
        simple_search.send_keys(Keys.RETURN)

    def advance_search_input(self,fqdn,arch,status):
        driver=self.driver
        driver.find_element_by_id("showadvancedsearch").click()
        driver.implicitly_wait(2)
        table=WebDriverSelect(driver.find_element_by_id("systemsearch_0_table"))
        table.select_by_value("System/Name")
        operation=WebDriverSelect(driver.find_element_by_id("systemsearch_0_operation"))
        operation.select_by_value("contains")
        value=driver.find_element_by_id("systemsearch_0_value")
        value.send_keys(fqdn)
        driver.find_element_by_xpath("//a[@id='doclink']").click()
        driver.implicitly_wait(4)
        table=WebDriverSelect(driver.find_element_by_id("systemsearch_1_table"))
        table.select_by_value("System/Arch")
        operation=WebDriverSelect(driver.find_element_by_id("systemsearch_1_operation"))
        operation.select_by_value("contains")
        value=driver.find_element_by_id("systemsearch_1_value")
        value.send_keys(arch)
        driver.find_element_by_xpath("//a[@id='doclink']").click()
        driver.implicitly_wait(4)
        table=WebDriverSelect(driver.find_element_by_id("systemsearch_2_table"))
        table.select_by_value("System/Status")
        operation=WebDriverSelect(driver.find_element_by_id("systemsearch_2_operation"))
        operation.select_by_value("is")
        value=WebDriverSelect(driver.find_element_by_id("systemsearch_2_value"))
        value.select_by_value(status)

    def advance_search(self,fqdn,arch,status):
        self.advance_search_input(fqdn,arch,status)
        self.driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()

    def advance_and_toggle_search(self,fqdn,arch,status,type):
        self.advance_search_input(fqdn,arch,status)
        self.advance_toggle_add_type(type)
        self.driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()

    def advance_search_2(self,fqdn,arch,status):
        self.advance_search_input(fqdn,arch,status)
        self.driver.implicitly_wait(4)
        self.driver.find_element_by_xpath("//tr[@id='systemsearch_1']/td/a[@class='btn']").click()
        self.driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()

    def advance_toggle_add_type(self,type):
        self.driver.find_element_by_id("customcolumns").click()
        self.driver.implicitly_wait(4)
        self.driver.find_element_by_xpath("//input[@value='"+type+"']").click()

    def toggle_set_default(self):
        self.driver.find_element_by_id("showadvancedsearch").click() 
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID,'customcolumns')))
        self.driver.find_element_by_id("customcolumns").click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("selectdefault").click()
        self.driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()

    def test_system_page_all_simple_search(self):
        self.driver.get(config.hub_url)
        fqdn=self.get_first_fqdn_from_system_list()
        self.simple_search(fqdn)
        self.is_system_in_search_result(fqdn)

    def test_system_page_avaiable_simple_search(self):
        driver=self.driver
        driver.get(config.hub_url+"available/")
        fqdn=self.get_first_fqdn_from_system_list()
        self.simple_search(fqdn)
        self.is_system_in_search_result(fqdn)

    def test_system_page_free_simple_search(self):
        driver=self.driver
        driver.get(config.hub_url+"free/")
        fqdn=self.get_first_fqdn_from_system_list()
        self.simple_search(fqdn)
        self.is_system_in_search_result(fqdn)
    
    def test_system_page_avaiable_advance_search(self):
        driver=self.driver
        fqdn,arch,status=self.get_first_free_system_information()
        driver.get(config.hub_url+"available/")
        self.toggle_set_default()
        driver.get(config.hub_url+"available/")
        self.advance_search(fqdn,arch,status)
        self.is_system_in_search_result(fqdn)
        driver.get(config.hub_url+"available/")
        self.advance_search_2(fqdn,arch,status)
        self.is_system_in_search_result(fqdn)
        driver.get(config.hub_url+"available/")
        type="System/Owner"
        self.advance_and_toggle_search(fqdn,arch,status,type)
        self.is_type_in_search_result("Owner")
        driver.get(config.hub_url+"available/")
        self.toggle_set_default()

    def test_system_page_free_advance_search(self):
        driver=self.driver
        fqdn,arch,status=self.get_first_free_system_information()
        driver.get(config.hub_url+"free/")
        self.toggle_set_default()
        driver.get(config.hub_url+"free/")
        self.advance_search(fqdn,arch,status)
        self.is_system_in_search_result(fqdn)
        driver.get(config.hub_url+"free/")
        self.advance_search_2(fqdn,arch,status)
        self.is_system_in_search_result(fqdn)
        driver.get(config.hub_url+"free/")
        type="System/Owner"
        self.advance_and_toggle_search(fqdn,arch,status,type)
        self.is_type_in_search_result("Owner")
        driver.get(config.hub_url+"free/")
        self.toggle_set_default()
    
    def test_system_page_all_advance_search(self):
        driver=self.driver
        fqdn,arch,status=self.get_first_free_system_information()
        driver.get(config.hub_url)
        self.toggle_set_default()
        driver.get(config.hub_url)
        self.advance_search(fqdn,arch,status)
        self.is_system_in_search_result(fqdn)
        driver.get(config.hub_url)
        self.advance_search_2(fqdn,arch,status)
        self.is_system_in_search_result(fqdn)
        driver.get(config.hub_url)
        type="System/Owner"
        self.advance_and_toggle_search(fqdn,arch,status,type)
        self.is_type_in_search_result("Owner")
        driver.get(config.hub_url)
        self.toggle_set_default()

    def tearDown(self):
        self.driver.close()

suite = unittest.TestLoader().loadTestsFromTestCase(BeakerSystemTest)
unittest.TextTestRunner(verbosity=2).run(suite)
#if __name__ == '__main__':
#    unittest.main()
