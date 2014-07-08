from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf  import settings

from UnchainedMessenger import views

urlpatterns = patterns('',
    url(r'^chat/$', views.BaseChatView.as_view(), name='base_chat'),

    url(r'^userchat/$', views.UserChatView.as_view(), name='user_chat'),
    url(r'^userchat/(?P<chatpartner>[a-zA-Z_0-9]+)/$', views.UserChatView.as_view(), name='user_chat'),

    url(r'^groupchat/(?P<group>[a-zA-Z_0-9]+)/$', views.GroupChatView.as_view(), name='group_chat'),
    url(r'^groupchat/$', views.GroupChatView.as_view(), name='group_chat'),
    url(r'^broadcastchat/$', views.BroadcastChatView.as_view(), name='broadcast_chat'),
    url(r'^login/$', views.login_user),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logged_out.html'}),
    url(r'^register/$', views.register),

	url(r'^$', views.index, name='index')
)