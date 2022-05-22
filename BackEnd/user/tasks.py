"""
@Description : 
@File        : tasks.py
@Project     : BackEnd
@Time        : 2022/5/18 17:47
@Author      : LiHouJian
@Software    : PyCharm
@issue       : 
@change      : 
@reason      : 
"""


from tools.sms import YunTongXin
from dadablog.celery import app


@app.task
def send_sms_c(phone, code):
	params = {
		'accountSid': '8a216da8806f31ad0180cd84c3621699',  # 这些配置项最好统一放在settings.py中
		'accountToken': '65ce95194dfc49b190a43ceeb2d2d8ce',
		'appId': '8a216da8806f31ad0180cd84c45016a0',
		'templateId': '1'
	}
	yun = YunTongXin(**params)
	res = yun.run(phone, code)
	return res