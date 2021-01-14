#!/usr/bin/env python
# -*- coding: utf-8 -*-

import undetected_chromedriver as uc
import json
from os.path import exists
import time


LOGIN_URL = 'https://elearning.warwick.nsw.edu.au/login/index.php'

SESSION_URL = 'https://elearning.warwick.nsw.edu.au/mod/bigbluebuttonbn/view.php?id=16150'
# SESSION_URL = 'https://elearning.warwick.nsw.edu.au/mod/bigbluebuttonbn/view.php?id=11375'

driver = uc.Chrome()


def login():
	driver.implicitly_wait(10)
	driver.get(LOGIN_URL)
	
	secrets = load_dict_file("__secrets.json")

	username_input = driver.find_element_by_name('username')
	username_input.send_keys(secrets["username"])
	pwd_input = driver.find_element_by_name('password')
	pwd_input.send_keys(secrets["password"])
	
	btn_login = driver.find_element_by_id("loginbtn")
	btn_login.click()


def getin_session():
	driver.get(SESSION_URL)
	
	btn_session = driver.find_element_by_id('join_button_input')
	btn_session.click()

	driver.switch_to.window(driver.window_handles[-1])
	btn_close_popup = driver.find_element_by_xpath('/html/body/div[2]/div/div/header/button')
	btn_close_popup.click()

	# wait for connection


def mark_attendance():
	# check if chat is displayed, otherwise open it
	btn_public_chat = driver.find_element_by_css_selector('[class^=chatListItem]')
	if not 'active' in btn_public_chat.get_attribute('class'):
		btn_public_chat.click()

	text_area = driver.find_element_by_css_selector('form div textarea#message-input')
	btn_send = driver.find_element_by_css_selector('form div textarea#message-input + button')

	att_details = load_dict_file("__attendance_details.json")

	text_area.send_keys(att_details.get("attendance_message"))
	btn_send.click()


def logout():
	# btn_dropdown = driver.find_element_by_id("dropdown-1")
	# btn_dropdown.click()

	# btn_logout = driver.find_element_by_xpath('/html/body/nav/ul[2]/li[2]/div/div/div/div/div/a[7]')
	# btn_logout.click()
	
	driver.quit()


def schedule(n,delay):
	for i in range(n):
		time.sleep(delay)
		print('event')
		mark_attendance()


def load_dict_file(filename):
        if exists(filename):
            with open(filename, "r", encoding="utf8") as exam_file:
                file_content = exam_file.read()
                reading_dict = dict()
                try:
                    temp_dict = json.loads(file_content)
                    reading_dict = temp_dict
                except json.decoder.JSONDecodeError as er:
                    print('Corrupted JSON file...')
        else:
            reading_dict = dict()

        return reading_dict


def test():
	login()
	getin_session()
	# mark_attendance()

	# logout()


if __name__ == '__main__':
	pass
	test()
