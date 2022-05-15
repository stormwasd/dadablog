from django.db import models
import random


def default_sign():
	signs = ['来吧，兄弟', '奔跑吧，兄弟']
	return random.choice(signs)

# Create your models here.
class UserProfile(models.Model):  # 用户配置

	username = models.CharField(max_length=11, verbose_name='用户名', primary_key=True)  # 用户名设为主键
	nickname = models.CharField(max_length=30, verbose_name='昵称')  # 昵称部分如果不希望有重名昵称可以加唯一索引
	password = models.CharField(max_length=32)  # 使用MD5加密，所以长度必须设置为32
	email = models.EmailField()
	phone = models.CharField(max_length=11)
	avatar = models.ImageField(upload_to='avatar', null=True)  # 和FileField类似，ImageField优点在于能重新定义图片的大小(图片长宽高定义)
	'''
	其实settings.py里面还少配置了两项，和文件上传相关的配置项，一个是media_url，一个
	是media_root，media_root指的是文件上传后存储到哪个位置，这里upload_to指定为avatar，
	也就是media_root下的avatar文件夹
	'''
	sign = models.CharField(max_length=50, verbose_name='个人签名', default=default_sign)
	info = models.CharField(max_length=150, verbose_name='个人简介', default='')
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)

	# 用元类改下表名
	class Meta:
		db_table = 'user_user_profile'  # 规范: 应用名_模型类名(驼峰拆开)

