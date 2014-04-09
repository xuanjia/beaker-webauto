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

class BeakerCommonLib(object):
    @staticmethod
    def get_id_from_string(job_string):
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

    def open_firefox_with_user(self):
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

    def open_firefox_with_admin(self):
        profile = webdriver.FirefoxProfile(config.user_admin)
        profile.set_preference("browser.download.folderList",2)
        profile.set_preference("browser.download.manager.showWhenStarting",False)
        profile.set_preference("browser.download.dir", os.getcwd()+"/download")
        #set auto download xml file
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/xml")
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
        self.driver = webdriver.Firefox(profile)
        driver = self.driver
        driver.get(config.hub_url)
    
    def get_jobid_after_submit(self):
        driver=self.driver
        driver.implicitly_wait(30)
        job_string=driver.find_element_by_xpath("//div[@class='alert flash']").text
        p=re.compile(r': ')
        job_id=p.split(job_string)[1]
        return job_id

    def submit_job(self):
        driver=self.driver
        driver.get(config.hub_url+"jobs/new")
        driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        driver.implicitly_wait(10)
        job_xml_input=driver.find_element_by_name("textxml")
        job_xml_file=open('../selenium/demo.xml')
        try:
            job_xml_content=job_xml_file.read()
        finally:
            job_xml_file.close()
        job_xml_input.send_keys(job_xml_content)
        #click button "Queue"
        driver.find_element_by_xpath("//button[@class='btn btn-primary btn-block']").click()
        return self.get_jobid_after_submit()
    
    def cancel_job(self,job_id):
        driver=self.driver
        has_cancelled=False
        while not has_cancelled:
            driver.get(config.hub_url+"jobs/cancel?id=" + job_id)
            driver.find_element_by_id("cancel_job_msg").send_keys(job_id)
            driver.find_element_by_xpath("//input[@class='submitbutton']").click()
            anchor=driver.page_source.find("Successfully cancelled job")
            if anchor > 0 :
                has_cancelled=True
                driver.implicitly_wait(5)
    
    def wait_job_status(self, job_id, status):
        driver=self.driver
        xpath_job=self.search_xpath_by_jobid(job_id)
        count=1
        while status != driver.find_element_by_xpath(xpath_job+"/td[6]").text:
            if count > 10:
                return False
            time.sleep(5)
            driver.refresh()
            xpath_job=self.search_xpath_by_jobid(job_id)
            count=count+1
        return True
    
    def wait_job_end(self,job_id):
        driver=self.driver
        driver.get(config.hub_url+"jobs")
        xpath_job=self.search_xpath_by_jobid(job_id)
        job_status=driver.find_element_by_xpath(xpath_job+"/td[6]").text
        count=1
        while job_status != "Completed" and job_status != "Cancelled" and job_status != "Aborted" :
            time.sleep(60)
            count=count+1
            if count > 60:
                return False
            driver.refresh()
            xpath_job=self.search_xpath_by_jobid(job_id)
            job_status=driver.find_element_by_xpath(xpath_job+"/td[6]").text
        return True
    
    def mine_job(self):
        driver=self.driver
        #return the first job id
        driver.get(config.hub_url+"jobs/mine")
        return self.get_jobid_from_list(1)
    
    def open_job_page(self,job_id):
        self.driver.get(config.hub_url+"jobs/"+job_id)

    def search_xpath_by_jobid(self,job_id):
        driver=self.driver
        xpath="//tbody/tr"
        job_list=driver.find_elements_by_xpath(xpath)
        for i in range(len(job_list)):
            j=i+1
            job_tmp=self.get_jobid_from_list(j)
            if job_id == job_tmp:
                return "//tbody/tr[%s]" % j
        return ""
    
    def get_jobid_from_list(self,anchor):
        driver=self.driver
        xpath="//tbody/tr[%s]/td[1]/a[contains(@href,'./')]" % anchor
        job_string=driver.find_element_by_xpath(xpath).text
        job_id=self.get_id_from_string(job_string)
        return job_id

