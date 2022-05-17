"""
@Description : 
@File        : sms
@Project     : BackEnd
@Time        : 2022/5/17 15:30
@Author      : LiHouJian
@Software    : PyCharm
@issue       : 
@change      : 
@reason      : 
"""

import datetime
import hashlib
import base64
import requests  # 发HTTP或HTTPS请求，将Python网络相关的原生方法做了高度的封装
import json


class YunTongXin():
	base_url = 'https://app.cloopen.com:8883'

	def __init__(self, accountSid, accountToken, appId, templateId):
		self.accountSid = accountSid  # 账户id
		self.accountToken = accountToken  # 授权令牌
		self.appId = appId  # APPID
		self.templateId = templateId  # 模板id

	# 生成具体发请求的url
	def get_request_url(self, sid):
		# 业务url格式: /2013-12-26/Accounts/{accountSid}/SMS/{funcdes}?sig={SigParameter}
		url = self.base_url + '/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s' % (self.accountSid, sid)
		return url

	# 生成时间戳的方法独立出来
	def get_timestamp(self):
		# 生成时间戳
		return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

	def get_sig(self, timestamp):
		# 生成业务url中的sig
		s = self.accountSid + self.accountToken + timestamp
		m = hashlib.md5()  # 生成MD5的计算对象
		m.update(s.encode())  # 把明文丢进去，但是要注意，这里要传字节串
		return m.hexdigest().upper()  # 以16进制导出，并且是大写

	def get_request_header(self, timestamp):
		# 生成请求头
		s = self.accountSid + ':' + timestamp
		auth = base64.b64encode(s.encode()).decode()  # b64encode参数也是字节串，然后最终结果再转成字符串
		return {
			'Accept': 'application/json',
			'Content-Type': 'application/json;charset=utf-8',
			'Authorization': auth
		}
	def get_request_body(self, phone, code):
		# 构建请求体
		return {
			'to': phone,
			'appId': self.appId,
			'templateId': self.templateId,
			'datas': [code, "3"]  # 验证码，验证码几分钟内有效，这里固定为3分钟
		}

	def request_api(self, url, header, body):
		res = requests.post(url, headers=header, data=json.dumps(body))
		return res.text



	# run()方法用于测试
	def run(self, phone, code):
		# 获取时间戳
		timestamp = self.get_timestamp()
		# 生成签名
		sig = self.get_sig(timestamp)
		# 生成请求url
		url = self.get_request_url(sig)
		# print(url)
		header = self.get_request_header(timestamp)
		# print(header)
		# 生成请求体
		body = self.get_request_body(phone, code)
		# 发送请求
		result = self.request_api(url, header, body)
		return result
		# print(result)



if __name__ == '__main__':  # 脚本入口

	# 参数太多我们以字典传参
	# accountSid, accountToken, appId, templateId
	params = {
		'accountSid': '8a216da8806f31ad0180cd84c3621699',
		'accountToken': '65ce95194dfc49b190a43ceeb2d2d8ce',
		'appId': '8a216da8806f31ad0180cd84c45016a0',
		'templateId': '1'
	}
	yun = YunTongXin(**params)
	res = yun.run('18979685341', '991202')
	print(res)
