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

class BeakerJobsTest(unittest.TestCase):
    def setUp(self):
        profile = webdriver.FirefoxProfile(config.user_noadmin)
        self.driver = webdriver.Firefox(profile)
        driver = self.driver
        driver.get(config.hub_url)
        self.assertIn("Systems",driver.title)
    
    @staticmethod
    def get_jobid_from_string(job_string):
        p=re.compile(r':')
        job_id=p.split(job_string)[1]
        return job_id
    
    def get_jobid_from_list(self, anchor):
        xpath="//tbody/tr[%s]/td[1]/a[contains(@href,'./')]" % anchor
        job_string=self.driver.find_element_by_xpath(xpath).text
        job_id=self.get_jobid_from_string(job_string)
        return job_id
    
    def search_xpath_by_jobid(self, job_id):
        xpath="//tbody/tr"
        job_list=self.driver.find_elements_by_xpath(xpath)
        for i in range(len(job_list)):
            j=i+1
            job_tmp=self.get_jobid_from_list(j)
            if job_id == job_tmp :
                return "//tbody/tr[%s]" % j
        return ""
    def submit_job(self):
        driver = self.driver
        driver.get(config.hub_url+"jobs/new")
        self.assertIn("New Job", driver.title)
        
        #click submit button
        driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        self.assertIn("Clone Job",driver.title)
        #input demo.xml in the text file
        job_xml_input=driver.find_element_by_name("textxml")
        job_xml_file=open('./selenium/demo.xml')
        try:
            job_xml_content=job_xml_file.read()
        finally:
            job_xml_file.close()
        job_xml_input.send_keys(job_xml_content)\
        #click button "Queue"
        driver.find_element_by_xpath("//button[@class='btn btn-primary btn-block']").click()
        #check the new job id
        driver.implicitly_wait(30)
        self.assertIn("Success! job id:",driver.page_source)
        #get job id
        job_string=driver.find_element_by_xpath("//div[@class='alert flash']").text
        p=re.compile(r': ')
        job_id=p.split(job_string)[1]
        return job_id

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
        job_id=self.get_jobid_from_string(job_string)
        return job_id
    
    def wait_job_status(self, job_id, status):
        driver=self.driver
        xpath_job=self.search_xpath_by_jobid(job_id)
        count=1
        while status != driver.find_element_by_xpath(xpath_job+"/td[6]").text:
            if count > 10:
                return False
            driver.implicitly_wait(10)
            driver.refresh()
            xpath_job=self.search_xpath_by_jobid(job_id)
            count=count+1
        return True
    
    def mine_job(self):
        #return the first job id
        driver=self.driver
        driver.get(config.hub_url+"jobs/mine")
        return self.get_jobid_from_list(1)
    
    def test_cancel_job(self):
        #submit a job
        job_id=self.submit_job()
        #open mine_job
        self.mine_job()
        #get xpath of job_id
        xpath_job=self.search_xpath_by_jobid(job_id)
        job_status=self.driver.find_element_by_xpath(xpath_job+"/td[6]").text
        if job_status == "Queued" or job_status == "New" or job_status == "Processed" or job_status == "Running" or job_status == "Waiting" or job_status == "Scheduled" :
        #click cancel button
            self.driver.find_element_by_xpath(xpath_job+"/td[8]/div/a[2]").click()
            self.assertIn("Cancel Job",self.driver.title)
            self.assertIn(job_id,self.driver.title)
            self.driver.find_element_by_id("cancel_job_msg").send_keys(job_id)
            self.driver.find_element_by_xpath("//input[@class='submitbutton']").click()
            self.assertIn("Successfully cancelled job",self.driver.page_source)
    
    def test_delete_job(self):
        #submit a job
        job_id=self.submit_job()
        #open mine_job
        self.mine_job()
        #cancel this job
        self.cancel_job(job_id)
        #wait job's status
        self.assertEqual(True,self.wait_job_status(job_id, "Cancelled"))
        #get xpath of job_id
        xpath_job=self.search_xpath_by_jobid(job_id)
        job_status=self.driver.find_element_by_xpath(xpath_job+"/td[6]").text
        if job_status == "Cancelled" or job_status == "Aborted" or job_status == "Completed" :
            #click delete button
            self.driver.find_element_by_xpath(xpath_job+"/td[8]/div/a[2]").click()
            time.sleep(10)
            self.driver.find_element_by_xpath("//div[@class='ui-dialog-buttonset']/button[1]").click()
            time.sleep(10)
            self.driver.refresh()
            self.assertNotIn(job_id,self.driver.page_source)

    def test_export_job(self):
        #submit a job
        job_id=self.submit_job()
        #open mine_job
        self.mine_job()
        #get xpath of job_id
        xpath_job=self.search_xpath_by_jobid(job_id)
        #click "Export" button
        self.driver.find_element_by_xpath(xpath_job+"/td[8]/div/a[3]").click()
        #String script = "document.getElementById('fileName').value='" + "/root/Beaker/beaker-auto/demo.xml" + "';";
        #((IJavascriptExecutor)driver).executeScript(script);
    
    def tearDown(self):
        pass
        #self.driver.close()

suite = unittest.TestLoader().loadTestsFromTestCase(BeakerJobsTest)
unittest.TextTestRunner(verbosity=2).run(suite)
