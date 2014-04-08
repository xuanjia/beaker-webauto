import unittest
import os
import string
import re
import config
import time
import glob
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select as WebDriverSelect

class BeakerTasksTest(unittest.TestCase):
    def setUp(self):
        profile = webdriver.FirefoxProfile(config.user_noadmin)
        profile.set_preference("browser.download.folderList",2)
        profile.set_preference("browser.download.manager.showWhenStarting",False)
        profile.set_preference("browser.download.dir", os.getcwd()+"/download")
        #set auto download xml file
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/xml")
        self.driver = webdriver.Firefox(profile)
        driver = self.driver
        driver.get(config.hub_url)
        self.assertIn("Systems",driver.title)
        os.system("sed -i -e s/VERSION=1.*/VERSION=1.0/g ./task/Makefile")
    
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

    def get_jobid_from_list(self, anchor):
        xpath="//tbody/tr[%s]/td[1]/a[contains(@href,'./')]" % anchor
        job_string=self.driver.find_element_by_xpath(xpath).text
        job_id=self.get_id_from_string(job_string)
        return job_id

    def get_jobid_after_submit(self):
        driver=self.driver
        driver.implicitly_wait(30)
        self.assertIn("Success! job id:",driver.page_source)
        #get job id
        job_string=driver.find_element_by_xpath("//div[@class='alert flash']").text
        p=re.compile(r': ')
        job_id=p.split(job_string)[1]
        return job_id
    
    def search_xpath_by_jobid(self, job_id):
        xpath="//tbody/tr"
        job_list=self.driver.find_elements_by_xpath(xpath)
        for i in range(len(job_list)):
            j=i+1
            job_tmp=self.get_jobid_from_list(j)
            if job_id == job_tmp:
                return "//tbody/tr[%s]" % j
        return ""

    def submit_job(self):
        driver = self.driver
        driver.get(config.hub_url+"jobs/new")
        self.assertIn("New Job", driver.title)
        
        #click submit button
        driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        #self.assertIn("Clone Job",driver.title)
        #input demo.xml in the text file
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

    def cancel_job(self, job_id):
        driver=self.driver
        has_cancelled=False
        while not has_cancelled:
            driver.get(config.hub_url+"jobs/cancel?id=" + job_id)
            #self.assertIn("Cancel Job", driver.title)
            #self.assertIn(job_id, driver.title)
            driver.find_element_by_id("cancel_job_msg").send_keys(job_id)
            driver.find_element_by_xpath("//input[@class='submitbutton']").click()
            #ensure this page is cancelled.
            anchor=driver.page_source.find("Successfully cancelled job")
            if anchor > 0 :
                has_cancelled=True
                driver.implicitly_wait(5)
    
    def clone_job(self, job_id):
        driver=self.driver
        driver.get(config.hub_url+"jobs/clone?id=" + job_id)
        driver.find_element_by_xpath("//button[@class='btn btn-primary btn-block']").click()
        #check the new job id
        driver.implicitly_wait(30)
        self.assertIn("Success! job id:", driver.page_source)
        #get job id
        job_string=driver.find_element_by_xpath("//div[@class='alert flash']").text
        job_id=self.get_id_from_string(job_string)
        return job_id
    
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
        #return the first job id
        driver=self.driver
        driver.get(config.hub_url+"jobs/mine")
        return self.get_jobid_from_list(1)

    def open_job_page(self,job_id):
        self.driver.get(config.hub_url+"jobs/"+job_id)

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
        driver.get(config.hub_url+'tasks/')
        task_name="beaker-client"
        self.task_simple_search(task_name)
        self.assertIn(task_name,driver.find_element_by_xpath("//tr[1]/td[1]/a[contains(@href ,'./')]").text)

    def test_task_libray_advance_search(self):
        driver=self.driver
        driver.get(config.hub_url+'tasks/')
        task_name="beaker-client"
        task_type="Sanity"
        task_description="beaker client testing"
        self.task_advance_search(task_name,task_type,task_description)
        self.assertIn(task_name,driver.find_element_by_xpath("//tr[1]/td[1]/a[contains(@href ,'./')]").text)
        driver.get(config.hub_url+'tasks/')
        self.task_advance_search_2(task_name,task_type,task_description)
        self.assertIn(task_name,driver.find_element_by_xpath("//tr[1]/td[1]/a[contains(@href ,'./')]").text)

    def test_new_task(self):
	driver=self.driver
        driver.get(config.hub_url+"/tasks/new")
        os.system("pushd task;rm -rf *.rpm ;make package >> /dev/null ;popd")
        package_name=''.join(self.get_task_rpm_package_path(os.getcwd()))
        driver.find_element_by_id("task_task_rpm").send_keys(package_name)
        driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        self.assertIn("/CoreOS/task/Sanity/beaker-web-automation Added/Updated",driver.page_source)

    def test_newer_task(self):
        driver=self.driver
        driver.get(config.hub_url+"/tasks/new")
        os.system("pushd task;rm -rf *.rpm ;sed -i -e s/VERSION=1.*/VERSION=1.2/g Makefile;make package >> /dev/null ;popd")
        package_name=''.join(self.get_task_rpm_package_path(os.getcwd()))
        driver.find_element_by_id("task_task_rpm").send_keys(package_name)
        driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        self.assertIn("/CoreOS/task/Sanity/beaker-web-automation Added/Updated",driver.page_source)
    
    def test_old_task(self):
        driver=self.driver
        driver.get(config.hub_url+"/tasks/new")
        os.system("pushd task;rm -rf *.rpm ;sed -i -e s/VERSION=1.*/VERSION=1.1/g Makefile >> /dev/null ;make package;popd")
        package_name=''.join(self.get_task_rpm_package_path(os.getcwd()))
        driver.find_element_by_id("task_task_rpm").send_keys(package_name)
        driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        self.assertIn("/CoreOS/task/Sanity/beaker-web-automation Added/Updated",driver.page_source)

    def tearDown(self):
        #pass
        self.driver.close()

#suite = unittest.TestLoader().loadTestsFromTestCase(BeakerTasksTest)
#unittest.TextTestRunner(verbosity=2).run(suite)
if __name__ == '__main__':
    unittest.main()
