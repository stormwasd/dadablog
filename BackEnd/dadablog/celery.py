"""
@Description : 
@File        : celery.py
@Project     : BackEnd
@Time        : 2022/5/18 17:35
@Author      : LiHouJian
@Software    : PyCharm
@issue       : 
@change      : 
@reason      : 
"""

from celery import Celery
from django.conf import settings
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'dadablog.settings')

# 初始化app
app = Celery('dadablog')  # 一般和django项目同名

# 一种新的配置方法
app.conf.update(
	BROKER_URL = 'redis://:@127.0.0.1:6379/1'
)

# 在每个应用下创建task的话就要使用下面的配置，不然生产者找不到
app.autodiscover_tasks(settings.INSTALLED_APPS)
