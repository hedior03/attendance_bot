#!/usr/bin/env python
# -*- coding: utf-8 -*-

import undetected_chromedriver as uc
import json
from os.path import exists


LOGIN_URL = 'https://elearning.warwick.nsw.edu.au/login/index.php'

SESSION_URL = 'https://elearning.warwick.nsw.edu.au/mod/bigbluebuttonbn/view.php?id=16150'

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

	# skip audio or microphone selection


def mark_attendance():
	# select public chat
	# click if it is not deployed

	# select textbox
	# type attendance details

	# select send button
	# send click


def logout():
	btn_dropdown = driver.find_element_by_id("dropdown-1")
	btn_dropdown.click()
	
	btn_logout = driver.find_element_by_xpath('/html/body/nav/ul[2]/li[2]/div/div/div/div/div/a[7]')
	btn_logout.click()
	
	driver.quit()


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


def main():
	login()

	# logout()


if __name__ == '__main__':
	main()
