"""
@Description : 
@File        : urls.py
@Project     : BackEnd
@Time        : 2022/5/19 11:07
@Author      : LiHouJian
@Software    : PyCharm
@issue       : 
@change      : 
@reason      : 
"""
from django.urls import path
from . import views

urlpatterns = [
	path('<str:author_id>', views.TopicViews.as_view())
]
