from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf  import settings

from UnchainedMessenger import views

urlpatterns = patterns('',
    url(r'^chat/$', views.BaseChatView.as_view(), name='base_chat'),

    url(r'^test/(?P<username>[a-zA-Z_0-9]+)/$', views.test, name='test'),

    url(r'^userchat/$', views.UserChatView.as_view(), name='user_chat'),


    url(r'^groupchat(?P<group>[a-zA-Z_0-9]+)/$', views.GroupChatView.as_view(), name='group_chat'),
    url(r'^broadcastchat/$', views.BroadcastChatView.as_view(), name='broadcast_chat'),



	url(r'^$', views.index, name='index')
)