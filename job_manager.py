#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

TIME_FORMAT = '%H:%M:%S'
FULL_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

scheduler = object()


def get_time_list(str_time_list):
	today = datetime.now().today()
	return [datetime.combine(today, datetime.strptime(tt, TIME_FORMAT).time()) for tt in str_time_list]


def tick(text):
    print(text + '! The time is: %s' % datetime.now())


def setup_jobs(str_time_list, fnc=tick, fnc_args=['TICKS']):
	global scheduler
	
	scheduler = BackgroundScheduler()

	time_list = get_time_list(str_time_list)	

	for tt in time_list:
		scheduler.add_job(fnc, 'date',run_date=tt, args=fnc_args)

	scheduler.start()


if __name__ == '__main__':
	test_list = [
		"16:38:48",
		"16:38:49"
	]
	setup_jobs(test_list)

	try:
	    while True:
	        time.sleep(2)
	except KeyboardInterrupt:
	    scheduler.shutdown()
