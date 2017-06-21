from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^search_index/$', views.get_search_form, name='search_index'),
	url(r'^search_trends/$', views.trends_search, name='search_trends'),
	url(r'^trends/$', views.trends, name='trends'),
	url(r'^saved_items/$', views.saved_items, name='saved_items'),
	url(r'^saved_user_tweets/(?P<userId>[0-9]+)/$', views.saved_tweets, name='saved_user_tweets'),
	url(r'^saved_keyword_tweets/(?P<keyword>[#?\w+\s\w+]+)/$', views.saved_keyword_tweets, name='saved_keyword_tweets'),
	url(r'^analyse_tweets/(?P<analysis_item>[#?\w+\s\w+]+)/$', views.analyse_tweets, name='analyse_tweets'),
]