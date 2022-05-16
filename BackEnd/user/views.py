import hashlib
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
# Create your views here.
from user.models import UserProfile
from tools.login_decrator import login_decrator


class UserViews(View):
	def get(self, request, username=None):
		if username:
			# /v1/users/guoxiaonao,拿到指定用户的的信息
			try:
				user = UserProfile.objects.get(username=username)
			except Exception as e:
				result = {'code': 10102, 'error': 'The username is wrong'}  # username是主键，查不到肯定是没有这个用户
				return JsonResponse(result)
			result = {'code': 200, 'username': username, 'data': {'info': user.info, 'sign': user.sign, 'nickname': user.nickname, 'avatar': str(user.avatar)}}
			return JsonResponse(result)
		else:
			# /v1/users,拿到所有用户的信息
			pass
		return JsonResponse({'code':200, 'msg': 'test'})

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

	def put(self, request, username=None):
		# 更新用户数据[昵称，个人签名，个人描述等]
		json_str = request.body
		json_obj = json.loads(json_str)

		try:
			user = UserProfile.objects.get(username=username)
		except Exception as e:
			result = {'code': 10105, 'error': 'The username is error'}
			return JsonResponse(result)
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
