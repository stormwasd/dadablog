"""
@Description : 
@File        : decrator_examle
@Project     : BackEnd
@Time        : 2022/5/20 17:15
@Author      : LiHouJian
@Software    : PyCharm
@issue       : 
@change      : 
@reason      : 
"""

import hashlib
import re
import urllib
import scrapy
import asyncio
import datetime
import os
import traceback
import json
from scrapy.utils import request
from lxml import etree
from scrapy.utils.project import get_project_settings
from pybase.util import send_file
import time


def get_func_time(get_time):
	def wrapper():
		start = time.time()
		get_time()
		end = time.time()
		msecs = (end - start) * 1000
		print("time is %d ms" % (msecs))

	# return get_add(*args, **kwargs)
	return wrapper


# simpletest
@get_func_time  # get_time = get_func_time(get_time)
def get_time():
	print("hello")
	time.sleep(1)
	print("world")


get_time()
