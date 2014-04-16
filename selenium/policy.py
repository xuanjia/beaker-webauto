import unittest
import os
import string
import re
import common
import time
import glob
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select as WebDriverSelect

class BeakerGroupPolicyTest(unittest.TestCase, common.BeakerCommonLib):
    def setUp(self):
        self.prepare_environment()
        self.open_firefox_with_user()
    
    def test_submit_group_job(self):
        driver=self.driver
        driver.get(self.hub_url+"jobs/new")
        driver.find_element_by_id("jobs_filexml").send_keys(os.getcwd()+"/group-demo.xml")
        driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
        driver.find_element_by_xpath("//button[@class='btn btn-primary btn-block']").click()
        #check the new job id
        job_id=self.get_jobid_after_submit()
        self.cancel_job(job_id)
        self.open_job_page(job_id)
        self.assertIn("web-auto", driver.page_source)
    
    def test_delegate_submit_job(self):
        driver=self.driver
        driver.get(self.hub_url+"prefs/")
        delegate_element=driver.find_element_by_id("SubmissionDelegates_user_text")
        delegate_element.send_keys(self.username_2_noadmin)
        delegate_element.send_keys(Keys.RETURN)
        self.driver.close()
        self.open_firefox_with_user_2()
        job_id=self.submit_job(user=self.username_1_noadmin)
        self.cancel_job(job_id)
        #check job list by user2
        self.assertTrue(self.find_job_in_mine_job_list(job_id))
        self.driver.close()
        #check job list by user1
        self.open_firefox_with_user()
        self.assertTrue(self.find_job_in_mine_job_list(job_id))
    
    def test_delegate_submit_job_invalid_user(self):
        driver=self.driver
        driver.get(self.hub_url+"prefs/")
        delegate_element=driver.find_element_by_id("SubmissionDelegates_user_text")
        delegate_element.send_keys(self.username_2_noadmin)
        delegate_element.send_keys(Keys.RETURN)
        self.driver.close()
        self.open_firefox_with_user_2()
        job_id=self.submit_job(user=self.username_3_noadmin)
        if job_id == u'0' and "not a valid submission delegate" in self.job_error :
            self.job_error=u''
            self.assertTrue(True)
        else :
            self.cancel_job(job_id)
            self.assertTrue(False)
        self.driver.close()
        #recover env
        self.open_firefox_with_user()
    
    def test_delegate_submit_group_job(self):
        driver=self.driver
        driver.get(self.hub_url+"prefs/")
        delegate_element=driver.find_element_by_id("SubmissionDelegates_user_text")
        delegate_element.send_keys(self.username_2_noadmin)
        delegate_element.send_keys(Keys.RETURN)
        self.driver.close()
        self.open_firefox_with_user_2()
        job_id=self.submit_job(user=self.username_1_noadmin,group=self.group_name)
        self.cancel_job(job_id)
        #check job list by user2
        #self.assertFalse(self.find_job_in_mine_group_job_list(job_id))
        self.assertTrue(self.find_job_in_mine_group_job_list(job_id))
        self.driver.close()
        #check job list by user1
        self.open_firefox_with_user()
        self.assertTrue(self.find_job_in_mine_group_job_list(job_id))

    def test_delegate_submit_invalid_group_job(self):
        driver=self.driver
        driver.get(self.hub_url+"prefs/")
        delegate_element=driver.find_element_by_id("SubmissionDelegates_user_text")
        delegate_element.send_keys(self.username_2_noadmin)
        delegate_element.send_keys(Keys.RETURN)
        self.driver.close()
        self.open_firefox_with_user_2()
        job_id=self.submit_job(user=self.username_1_noadmin,group="admin")
        if job_id == u'0' and "is not a member of group" in self.job_error :
            self.job_error = u''
            self.assertTrue(True)
        else :
            self.cancel_job(job_id)
            self.assertTrue(False)
        self.driver.close()
        #recover env
        self.open_firefox_with_user()
    
    def test_create_and_delete_and_update_group_by_admin(self):
        self.driver.close()
        self.open_firefox_with_admin()
        group_name="TestAutomation"
        self.assertTrue(self.create_group(group_name,"RedHat@4096"))
        self.add_group_memeber(group_name,self.username_3_noadmin)
        self.driver.get(self.hub_url+"groups/edit?group_name="+group_name)
        self.assertIn(self.username_3_noadmin, self.driver.page_source)
        self.remove_group_member(group_name,self.username_3_noadmin)
        self.driver.get(self.hub_url+"groups/edit?group_name="+group_name)
        #self.assertNotIn(self.username_3_noadmin, self.driver.page_source)
        self.change_group_password(group_name,"RedHat@j83a54")
        self.assertIn("OK",self.driver.page_source)
        self.delete_group(group_name)
        self.driver.get(self.hub_url+"groups/edit?group_name="+group_name)
        self.assertIn("Need a valid group to search on", self.driver.page_source)
   
    def action_access_policy_process_by_user(self,action,fqdn,access_policy,user):
        driver=self.driver
        table_list=driver.find_elements_by_xpath("//tbody[@class='user-rows']/tr/td[1]")
        for i in range(len(table_list)) :
            if user in table_list[i].text :
                break
        j=str(i+2)
        policy_list={'view':'2','edit_policy':'3','edit_system':'4','loan_any':'5','loan_self':'6','control_system':'7','reserve':'8'}
        access_policy_element=driver.find_element_by_xpath("//tbody[@class='user-rows']/tr["+j+"]/td["+policy_list[access_policy]+"]/input")
        if action == "set" :
            if not access_policy_element.is_selected() :
                access_policy_element.click()
                driver.find_element_by_xpath("//div[@id='access-policy']//div[@class='form-actions']/button[1]").click()
        elif action == "unset" :
            if access_policy_element.is_selected() :
                access_policy_element.click()
                driver.find_element_by_xpath("//div[@id='access-policy']//div[@class='form-actions']/button[1]").click()
        elif action == "check" :
            if not access_policy_element.is_selected():
                return False
            else:
                return True
    
    def action_access_policy_process_by_group(self,action,fqdn,access_policy,group):
        driver=self.driver
        table_list=driver.find_elements_by_xpath("//tbody[@class='group-rows']/tr/td[1]")
        for i in range(len(table_list)) :
            if user in table_list[i].text :
                break
        j=str(i+2)
        policy_list={'view':'2','edit_policy':'3','edit_system':'4','loan_any':'5','loan_self':'6','control_system':'7','reserve':'8'}
        access_policy_element=driver.find_element_by_xpath("//tbody[@class='group-rows']/tr["+j+"]/td["+policy_list[access_policy]+"]/input")
        if action == "set":
            if not access_policy_element.is_selected :
                access_policy_element.click()
                driver.find_element_by_xpath("//div[@id='access-policy']//div[@class='form-actions']/button[1]").click()
        elif action == "unset":
            if access_policy_element.is_selected :
                access_policy_element.click()
                driver.find_element_by_xpath("//div[@id='access-policy']//div[@class='form-actions']/button[1]").click()
        elif action == "check":
            if not access_policy_element.is_selected :
                return False
            else:
                return True
    
    def action_access_policy(self,action,fqdn,access_policy,user=None,group=None):
        driver=self.driver
        driver.get(self.hub_url+"view/"+fqdn+"#access-policy")
        time.sleep(20)
        if user != None :
            if action != "check" :
                user_input=driver.find_element_by_id("access-policy-user-input")
                user_input.send_keys(user)
                user_input.send_keys(Keys.RETURN)
                driver.find_element_by_xpath("//tbody[@class='user-rows']//button[@class='btn add']").click()
            self.action_access_policy_process_by_user(action,fqdn,access_policy,user)
            time.sleep(20)
        if group != None :
            if user != "check":
                group_input=driver.find_element_by_id("access-policy-group-input")
                group_input.send_keys(group)
                group_input.send_keys(Keys.RETURN)
                driver.find_element_by_xpath("//tbody[@class='group-rows']//button[@class='btn add']").click()    
            self.action_access_policy_process_by_group(action,fqdn,access_policy,group)     
            time.sleep(20)
        return True
      
    def test_access_policy_view_by_admin(self):
        self.driver.close()
        self.open_firefox_with_admin()
        fqdn="web.auto.com"
        self.create_new_system(fqdn)
        self.action_access_policy("set",fqdn,"view",user=self.username_1_noadmin)
        self.driver.get(self.hub_url+"view/"+fqdn+"#access-policy")
        WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.ID,"access-policy-user-input")))
        self.assertTrue(self.username_1_noadmin in self.driver.page_source)
        self.driver.close()
        self.open_firefox_with_user()
        self.driver.get(self.hub_url+"view/"+fqdn)
        self.assertTrue(self.action_access_policy("check",fqdn,"view",user=self.username_1_noadmin))
        self.driver.close()
        self.open_firefox_with_admin()
        self.action_access_policy("unset",fqdn,"view",user=self.username_1_noadmin)
        self.driver.close()
        self.open_firefox_with_user()
    def tearDown(self):
        #pass
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
