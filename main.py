#!/usr/bin/env python
# -*- coding: utf-8 -*-

import undetected_chromedriver as uc
import json
from os.path import exists

import job_manager


def login():
	driver.implicitly_wait(10)
	driver.get(ATT_DETAILS.get('login_url'))
	
	secrets = load_dict_file("__secrets.json")

	username_input = driver.find_element_by_name('username')
	username_input.send_keys(secrets["username"])
	pwd_input = driver.find_element_by_name('password')
	pwd_input.send_keys(secrets["password"])
	
	btn_login = driver.find_element_by_id("loginbtn")
	btn_login.click()


def getin_session():
	driver.get(ATT_DETAILS.get('session_url'))
	
	btn_session = driver.find_element_by_id('join_button_input')
	btn_session.click()

	driver.switch_to.window(driver.window_handles[-1])
	btn_close_popup = driver.find_element_by_xpath('/html/body/div[2]/div/div/header/button')
	btn_close_popup.click()

	# wait for connection


def mark_attendance():
	post_message(ATT_DETAILS.get("attendance_message"))


def post_message(msg):
	# check if chat is displayed, otherwise open it
	btn_public_chat = driver.find_element_by_css_selector('[class^=chatListItem]')
	if not 'active' in btn_public_chat.get_attribute('class'):
		btn_public_chat.click()

	text_area = driver.find_element_by_css_selector('form div textarea#message-input')
	btn_send = driver.find_element_by_css_selector('form div textarea#message-input + button')

	print(f'{job_manager.datetime.now()} >>> [post_message]\t{msg}')
	text_area.send_keys(msg)
	btn_send.click()


def logout():
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


def test_task_timing():
	job_manager.setup_jobs([ATT_DETAILS.get('start')], fnc_args=['START'])
	job_manager.setup_jobs(ATT_DETAILS.get('calls_time'))
	job_manager.setup_jobs([ATT_DETAILS.get('finish')], fnc_args=['FINISH'])


def schedule_task(time_list, fnc, fnc_args):
	job_manager.setup_jobs(time_list, fnc=fnc, fnc_args=fnc_args)


def main():
	global driver
	driver = uc.Chrome()

	login()
	getin_session()

	schedule_task([ATT_DETAILS.get('start')], fnc=post_message, fnc_args=[ATT_DETAILS.get('start_message')])
	schedule_task(ATT_DETAILS.get('calls_time'), fnc=mark_attendance, fnc_args=[])
	schedule_task([ATT_DETAILS.get('finish')], fnc=post_message, fnc_args=[ATT_DETAILS.get('finish_message')])



ATT_DETAILS = load_dict_file("__attendance_details.json")

driver = object()

if __name__ == '__main__':
	main()
