from django.db import models
from user.models import UserProfile

# Create your models here.

class Topic(models.Model):

	title = models.CharField(max_length=50, verbose_name='文章标题')
	# tec & no_tec
	category = models.CharField(max_length=20, verbose_name='文章分类')
	# public & private
	limit = models.CharField(max_length=20, verbose_name='文章权限')
	introduce = models.CharField(max_length=90, verbose_name='文章简介')
	content = models.TextField(verbose_name='文章内容')
	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)
	# 下面是外键关联,一对多
	# 第二个参数表示级联删除，要删一起删，user没了，那他的所有文章也一并会删除
	# 1. no action 表示 不做任何操作，
	# 2. set null 表示在外键表中将相应字段设置为null
	# 3. set default 表示设置为默认值
	# 4. cascade 表示级联操作，就是说，如果主键表中被参考字段更新，外键表中也更新，主键表中的记录被删除，外键表中改行也相应删除
	author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	# author叫外键属性名(绑定的时候给object)，数据库中的quthor_id叫外键字段名(绑定的时候给值)

