"""
@Description : 
@File        : cache_dec
@Project     : BackEnd
@Time        : 2022/5/20 15:46
@Author      : LiHouJian
@Software    : PyCharm
@issue       : 
@change      : 
@reason      : 
"""
from django.core.cache import cache

from .login_decrator import get_user_by_request


def cache_set(expire):
	def _cache_set(func):
		def wrapper(request, *args, **kwargs):
			# 区分场景 - 只做列表页
			if 't_id' in request.GET:
				# 当前请求是获取文章详情页
				return func(request, *args, **kwargs)
			# 生成出正确的cache_key区分访客访问和博主访问
			visitor_user = get_user_by_request(request)
			visitor_username = None
			if visitor_user:
				visitor_username = visitor_user.username
			author_username = kwargs['author_id']
			print('visitor is %s'%(visitor_username))
			print('author is %s'%(author_username))
			full_path = request.get_full_path()
			if visitor_username == author_username:
				cache_key = 'topics_cache_self_%s'%(full_path)  # 自己访问自己cachekey多一个self
			else:
				cache_key = 'topics_cache_%s'%(full_path)
			print(cache_key)
			# 判断是否有缓存，有缓存则直接返回
			res = cache.get(cache_key)
			if res:
				print('---cache in')  # 打印出这个说明当前肯定走的缓存
				return res
			# 执行视图
			res = func(request, *args, **kwargs)
			# 存储缓存 推荐使用cache对象/set/get
			cache.set(cache_key, res, expire)
			# 返回响应
			return res
		return wrapper
	return _cache_set