#Beaker Web Automation
This project is only for testing beaker's web console. The default browser is FireFox.

##Environment Requirement
* Python 2.7
* Selenium 2.4
* Firefox with AutoAuth plugin

##SetUp
*  Open selenium/config.py

>  hub_url=""#beaker's url

>  user_admin="../firefox/autouser1"#for username_admin profile

>  user_noadmin_1="../firefox/autouser2"#for username_1_noadmin profile

>  user_noadmin_2="../firefox/autouser3"#for username_2_noadmin profile

>  username_admin=""#admin user name

>  username_1_noadmin=""#noadmin user name 1

>  username_2_noadmin=""#noadmin user name 2

>  username_3_noadmin=""#noadmin user name 3

>  group_name="web-auto"#group name for username_1_noadmin

>  group_password="RedHat@beaker2013"#group password for group_name

* Create firefox profile under "firefox/autouser1" with username_admin account. And install AutoAuth plugin.

>  *Tip:* 
       [root@localhost ~]# firefox -P

* Open firefox with username_admin profile, and login beaker with admin account.Please save the password, then automation can work
* Same step for username_1_noadmin and username_2_noadmin

##Contract with me
* Xuan Jia (jason.jiaxuan@gmail.com)    
