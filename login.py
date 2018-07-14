#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 weihao <blackhatdwh@gmail.com>
#
# Distributed under terms of the MIT license.


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from ocr import recognize
import sys
from time import sleep
def login():
    options = webdriver.ChromeOptions()
    options.binary_location = '/usr/bin/google-chrome'
    options.add_argument('headless')
    options.add_argument('--window-size=800,600')
    driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=options)
    not_login = True
    driver.execute_script('window.open("");')       # open a new tab for CAPTCHA
    
    while not_login:
        driver.switch_to.window(driver.window_handles[0])       # switch to login page
        driver.get('http://www.pss-system.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml')
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'j_validation_code')))
        except TimeoutException:
            continue
    
        driver.find_element_by_id('j_username').send_keys('a729918410')
        driver.find_element_by_id('j_password_show').send_keys('HAF4cu0HkiaW')
        driver.switch_to.window(driver.window_handles[1])       # switch to code image
        
        while True:
            driver.get('http://www.pss-system.gov.cn/sipopublicsearch/portal/login-showPic.shtml')
            driver.save_screenshot('fuck.png')
            code = recognize()
            if code != 'wtf':
                break
        
        driver.switch_to.window(driver.window_handles[0])       # switch to login page
        driver.find_element_by_id('j_validation_code').send_keys(code)
        driver.execute_script('login();')
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-dialog-content')))
            error_dialog = driver.find_element_by_class_name('ui-dialog-content').text
            if error_dialog.find('密码') != -1:
                print('Password error. You are fucked')
                sys.exit()
            if error_dialog.find('验证码') != -1:
                print('CAPTCHA error. Try again.')
                continue
        except TimeoutException:
            try:
                driver.find_element_by_id('globleBody')
            except NoSuchElementException:
                continue
            print('Seems good.')
        
    
        not_login = False
        JSESSIONID = driver.get_cookie('JSESSIONID')
        WEE_SID = driver.get_cookie('WEE_SID')
        return {'JSESSIONID': JSESSIONID['value'], 'WEE_SID': WEE_SID['value']}

if __name__ == '__main__':
    print(login())