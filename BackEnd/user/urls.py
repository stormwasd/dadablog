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
	path("<str:username>", views.UserViews.as_view()),  # path转换器
	path("<str:username>/avatar", views.user_views)
]