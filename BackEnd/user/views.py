import hashlib
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
# Create your views here.
from user.models import UserProfile


class UserViews(View):
	# def get(self, request):
	# 	return JsonResponse({'code':200, 'msg': 'test'})

	def post(self, request):
		json_str = request.body
		json_obj = json.loads(json_str)
		username = json_obj.get('username')
		email = json_obj.get('email')
		password_1 = json_obj.get('password_1')
		password_2 = json_obj.get('password_2')
		phone = json_obj.get('phone')

		# 参数基本检查
		# 检查两次输入
		if password_1 != password_2:
			result = {'code': 10100, 'error': 'The password is not same~'}
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
		UserProfile.objects.create(username=username, nickname=username, password=p_m.hexdigest(), email=email, phone=phone)

		# 如果参数检查通过并存储完成
		result = {'code': 200, 'username': username, 'data': {}}
		return JsonResponse(result)