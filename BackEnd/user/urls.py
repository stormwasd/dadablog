"""
@Description : 
@File        : urls.py
@Project     : FrontEnd
@Time        : 2022/5/16 14:33
@Author      : LiHouJian
@Software    : PyCharm
@issue       : 
@change      : 
@reason      : 
"""


from django.urls import path
from . import views


urlpatterns = [
	# v1/users/sms, 这要注意，注册的时候sms这个用户名是不可用的
	path("sms", views.sms_view),
	path("<str:username>", views.UserViews.as_view()),  # path转换器
	path("<str:username>/avatar", views.user_views)
]