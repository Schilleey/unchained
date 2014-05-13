from django.conf.urls import patterns, url

from UnchainedMessenger import views

urlpatterns = patterns('',
    url(r'^chat/$', views.BroadcastChatView.as_view(), name='broadcast_chat'),
    url(r'^userchat/$', views.UserChatView.as_view(), name='user_chat'),
    url(r'^groupchat/$', views.GroupChatView.as_view(), name='group_chat'),
	url(r'^$', views.index, name='index'),
)