import hashlib
import json
import random

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
# Create your views here.
from user.models import UserProfile
from tools.login_decrator import login_decrator
from tools.sms import YunTongXin
from .tasks import send_sms_c

class UserViews(View):
	def get(self, request, username=None):
		if username:
			# /v1/users/guoxiaonao,拿到指定用户的的信息
			try:
				user = UserProfile.objects.get(username=username)
			except Exception as e:
				result = {'code': 10102, 'error': 'The username is wrong'}  # username是主键，查不到肯定是没有这个用户
				return JsonResponse(result)
			result = {'code': 200, 'username': username,
					  'data': {'info': user.info, 'sign': user.sign, 'nickname': user.nickname,
							   'avatar': str(user.avatar)}}
			return JsonResponse(result)
		else:
			# /v1/users,拿到所有用户的信息
			pass
		return JsonResponse({'code': 200, 'msg': 'test'})

	def post(self, request):
		json_str = request.body
		json_obj = json.loads(json_str)
		username = json_obj.get('username')
		email = json_obj.get('email')
		password_1 = json_obj.get('password_1')
		password_2 = json_obj.get('password_2')
		phone = json_obj.get('phone')
		sms_num = json_obj.get('sms_num')
		# print(sms_num)

		# 参数基本检查
		# 检查两次输入
		if password_1 != password_2:
			result = {'code': 10100, 'error': 'The password is not same~'}
			return JsonResponse(result)
		# 比对验证码是否正确
		old_code = cache.get('sms_%s'%(phone))
		# print(old_code)
		if not old_code:
			result = {'codd': '10100', 'error': 'The code is expired'}
			return JsonResponse(result)
		if int(sms_num) != old_code:
			result = {'codd': '10100', 'error': 'The code is wrong'}
			return JsonResponse(result)



		# 检查用户名是否可用
		old_users = UserProfile.objects.filter(username=username)  # 如果用get要try(防止没查到报错)，get是返回值，而filter是返回Queryset
		if old_users:
			result = {'code': 10101, 'error': 'The username is already existed!'}
			return JsonResponse(result)
		# user错误码范围: 10100-10199
		# 密码MD5存储
		p_m = hashlib.md5()  # 构建一个MD5对象
		p_m.update(password_1.encode())  # password_1是一个字符串，但是update()所接受的是字节串，所以需要使用encode()转换下

		# 32位MD5用hexdigest()转成16进制存储
		UserProfile.objects.create(username=username, nickname=username, password=p_m.hexdigest(), email=email,
								   phone=phone)

		# 如果参数检查通过并密码存储完成
		result = {'code': 200, 'username': username, 'data': {}}
		# 用户信息的记录还未完成
		return JsonResponse(result)

	@method_decorator(login_decrator)
	def put(self, request, username=None):
		# 更新用户数据[昵称，个人签名，个人描述等]
		json_str = request.body
		json_obj = json.loads(json_str)
		# 使用装饰器就不用下面的orm操作了
		# try:
		# 	user = UserProfile.objects.get(username=username)
		# except Exception as e:
		# 	result = {'code': 10105, 'error': 'The username is error'}
		# 	return JsonResponse(result)
		user = request.myuser
		user.sign = json_obj['sign']
		user.info = json_obj['info']
		user.nickname = json_obj['nickname']
		user.save()
		return JsonResponse({'code': 200})


@login_decrator
def user_views(request):  # 改头像
	if request.method != 'POST':
		result = {'code': 10103, 'error': 'Please use POST'}
		return JsonResponse(result)
	# 使用装饰器就不用下面的orm操作了
	# try:
	# 	user = UserProfile.objects.get(username=username)
	# except Exception as e:
	# 	result = {'code': 10104, 'error': 'The username is error'}
	# 	return JsonResponse(result)
	user = request.myuser

	avatar = request.FILES['avatar']  # 拿前端传过来的头像数据
	user.avatar = avatar
	user.save()
	return JsonResponse({'code': 200})


def sms_view(request):
	if request.method != 'POST':
		result = {'code': 10108, 'error': 'Please use POST'}
		return JsonResponse(result)
	json_str = request.body
	json_odj = json.loads(json_str)
	phone = json_odj['phone']

	# 生成随机数
	code = random.randint(1000, 9999)  # 4位数字
	print('phone', phone, 'code', code)
	# 存储随机码, 用django-redis(django缓存和redis给融合在一起)，之前django项目的缓存是用mysql的一张表进行存储，但在这个项目不适用
	cache_key = 'sms_%s' % (phone)  # 生成缓存的key
	old_code = cache.get(cache_key)  # 判断是否已经存在该手机号的缓存,为了防止用户一直刷新发验证码
	if old_code:
		return JsonResponse({'code': 10111, 'error': 'The code is already existed'})
	cache.set(cache_key, code, 60)
	# 发送随机码 -> 短信
	# send_sms(phone, code)  # 这里最好判断下状态码是否是000000，不是此状态码因该返回一个异常，现在的逻辑是铁定返回200，这逻辑上是不科学的
	send_sms_c.delay(phone, code)  # 这样依赖即使第三方平台阻塞了，Django一点影响也没有，可以迅速返回响应
	return JsonResponse({'code': 200})


def send_sms(phone, code):
	params = {
		'accountSid': '8a216da8806f31ad0180cd84c3621699',  # 这些配置项最好统一放在settings.py中
		'accountToken': '65ce95194dfc49b190a43ceeb2d2d8ce',
		'appId': '8a216da8806f31ad0180cd84c45016a0',
		'templateId': '1'
	}
	yun = YunTongXin(**params)
	res = yun.run(phone, code)
	return res
