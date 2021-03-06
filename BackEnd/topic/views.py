import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator  # 把原来的函数装饰器转换下
from django.views.decorators.cache import cache_page

from tools.login_decrator import login_decrator, get_user_by_request
from tools.cache_dec import cache_set

# 异常码 10300-10399

# Create your views here.

# 创建视图类
from topic.models import Topic
from user.models import UserProfile


class TopicViews(View):

	def make_topic_res(self, author, author_topic, is_self):
		"""
		:param author:
		:param author_topic:
		:return:
		"""

		if is_self:
			# 博主访问自己
			next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author).first()  # .first()方法就把数据从小到大排列并取第一个
			last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author).last()  # .last()方法就把数据从大到小排列并取第一个
		else:
			# 访客访问
			next_topic = Topic.objects.filter(id__gt=author_topic.id,
											  author=author, limit='public').first()  # .first()方法就把数据从小到大排列并取第一个
			last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author, limit='public').last()  # .last()方法就把数据从大到小排列并取第一个
		next_id = next_topic.id if next_topic else None
		next_title = next_topic.title if next_topic else ''
		last_id = last_topic.id if last_topic else None
		last_title = last_topic.title if last_topic else ''
		res = {'code': 200, 'data': {}}
		res['data']['nickname'] = author.nickname
		res['data']['title'] = author_topic.title
		res['data']['category'] = author_topic.category
		res['data']['created_time'] = author_topic.create_time.strftime('%Y-%m-%d %H:%M:%S')
		res['data']['content'] = author_topic.content
		res['data']['introduce'] = author_topic.introduce
		res['data']['author'] = author.nickname
		res['data']['last_id'] = last_id
		res['data']['last_title'] = last_title
		res['data']['next_id'] = next_id
		res['data']['next_title'] = next_title
		res['data']['messages'] = []
		res['data']['messages_count'] = 0
		return res


	def make_topics_res(self, author, author_topics):
		"""
		:return: 返回列表页数据
		"""
		# 不管是登录用户还是游客，都返回limit的topic

		topics_res = list()
		for topic in author_topics:
			topics_dict = dict()
			topics_dict['id'] = topic.id
			topics_dict['title'] = topic.title
			topics_dict['category'] = topic.category
			topics_dict['created_time'] = topic.create_time.strftime("%Y-%m-%d %H:%M:%S")
			topics_dict['introduce'] = topic.introduce
			topics_dict['author'] = author.nickname
			topics_res.append(topics_dict)

		result = {'code': 200, 'data': {'nickname': author.nickname, 'topics': topics_res}}
		return result

	@method_decorator(login_decrator)
	def post(self, request, author_id):
		author = request.myuser
		# 取出前端数据
		json_str = request.body
		# 将json字符串转换成json对象，也就对应着python中的字典
		json_obj = json.loads(json_str)
		# 然后就是取数据
		title = json_obj['title']
		content = json_obj['content']
		content_text = json_obj['content_text']
		introduce = content_text[:30]  # 截取前三十个字符
		limit = json_obj['limit']
		category = json_obj['category']
		if limit not in ['public', 'private']:  # 不是这两种就是违法请求
			result = {'code': 10300, 'error': 'The limit error~'}
			return JsonResponse(result)
		# 创建topic数据
		Topic.objects.create(title=title, content=content, limit=limit, category=category, introduce=introduce,
							 author=author)
		return JsonResponse({'code': 200})

	@method_decorator(cache_set(30))
	def get(self, request, author_id):
		print('......view...in......')
		try:
			author = UserProfile.objects.get(username=author_id)
		except Exception as e:
			result = {'code': 10301, 'error': 'The author is not existed'}
			return JsonResponse(result)

		visitor = get_user_by_request(request)  # 判断是博主还是登录但非博主还是游客
		visitor_username = None  # 游客默认为None
		if visitor:
			visitor_username = visitor.username

		t_id = request.GET.get('t_id')
		if t_id:
			# /v1/topics/storm?t_id=1
			# 获取指定文章数据
			t_id = int(t_id)
			is_self = False
			if visitor_username == author_id:
				is_self = True
				try:
					author_topic = Topic.objects.get(id=t_id, author_id=author_id)
				except Exception as e:
					result = {'code': 10302, 'error': 'No topic'}
					return JsonResponse(result)
			else:  # 非博主只能访问public
				try:
					author_topic = Topic.objects.get(id=t_id, author_id=author_id, limit='public')
				except Exception as e:
					result = {'code': 10303, 'error': 'No topic'}
					return JsonResponse(result)

			res = self.make_topic_res(author, author_topic, is_self)
			return JsonResponse(res)

		else:
			# 获取列表页数据
			category = request.GET.get('category')
			if category in ['tec', 'no-tec']:
				if visitor_username == author_id:
					# 博主访问自己的博客
					author_topics = Topic.objects.filter(author_id=author_id, category=category)
				else:
					author_topics = Topic.objects.filter(author_id=author_id, limit='public', category=category)
				res = self.make_topics_res(author, author_topics)
				return JsonResponse(res)
			else:
				if visitor_username == author_id:
					# 博主访问自己的博客
					author_topics = Topic.objects.filter(author_id=author_id)
				else:
					author_topics = Topic.objects.filter(author_id=author_id, limit='public')

				res = self.make_topics_res(author, author_topics)
				return JsonResponse(res)
