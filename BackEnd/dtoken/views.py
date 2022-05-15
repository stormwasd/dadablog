import hashlib

from django.http import JsonResponse
from django.shortcuts import render
import json
from user.models import UserProfile
# 异常码 10200-10299
# Create your views here.
def tokens(request):
	if request.method != 'POST':
		result = {'code': 10200, 'error': 'Please use POST!'}
		return JsonResponse(result)
	json_str = request.body
	json_obj = json.loads(json_str)
	username = json_obj.get('username')
	password = json_obj.get('password')
	# 校验用户名和密码(这里用下get)
	try:
		user = UserProfile.objects.get(username=username)
	except Exception as e:
		result = {'code': 10201, 'error': 'The username or password is wrong!'}
		return JsonResponse(result)
	# 如果username没有报异常，那就接着判断password
	p_m = hashlib.md5()
	p_m.update(password.encode())
	if p_m.hexdigest() != user.password:
		result = {'code': 10202, 'error': 'The username or password is wrong!'}
		return JsonResponse(result)
	# 记录会话状态
	result = {'code': 200, 'username': username, 'data': {}}
	return JsonResponse(result)
