from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.template import RequestContext

from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt

from ws4redis.publisher import RedisPublisher

# Create your views here.

def index(request):

    return render_to_response("index.html")

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view(), redirect_field_name=None)

class BaseChatView(LoginRequiredMixin, TemplateView):
    template_name = 'base_chat.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(BaseChatView,self).get_context_data(**kwargs)
        context.update(groups=Group.objects.all())
        context.update(users=User.objects.all().exclude(username=user.username))
        return context


class BroadcastChatView(LoginRequiredMixin, TemplateView):
    template_name = 'broadcast_chat.html'

    def get(self, request, *args, **kwargs):
        username = self.request.user.username
        RedisPublisher(facility='unchained', broadcast=True).publish_message(username + ': ' + 'Hello everybody')  # send a welcome message to everybody
        return super(BroadcastChatView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(BroadcastChatView, self).get_context_data(**kwargs)
        context.update(users=User.objects.all().exclude(username=user.username))
        context.update(groups=Group.objects.all())
        context.update(username=user.username)
        return context

class UserChatView(LoginRequiredMixin, TemplateView):
    template_name = 'user_chat.html';

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(UserChatView, self).get_context_data(**kwargs)
        context.update(users=User.objects.all().exclude(username=user.username))
        context.update(groups=Group.objects.all())
        context.update(chatpartner=kwargs['chatpartner'])
        context.update(username=user.username)
        return context

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        redis_publisher = RedisPublisher(facility='unchained', users=[request.POST.get('user')])
        redis_publisher.publish_message(request.POST.get('message'))
        return HttpResponse('OK')


class GroupChatView(LoginRequiredMixin, TemplateView):
    template_name = 'group_chat.html'

    def get_context_data(self, **kwargs):
        context = super(GroupChatView, self).get_context_data(**kwargs)
        context.update(groups=Group.objects.all())
        context.update(users=User.objects.all())
        print(kwargs)
        return context

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        redis_publisher = RedisPublisher(facility='unchained', groups=[request.POST.get('group')])
        redis_publisher.publish_message(request.POST.get('message'))
        return HttpResponse('OK')


def login_user(request):
    state = "Please log in below..."
    redirect = 0
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                redirect = 1
                state = "You're successfully logged in! You will be redirected soon."
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render_to_response('login.html',
                              {'state':state, 'username': username, 'redirect': redirect},
                              context_instance=RequestContext(request))


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/login/")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {'form': form, })
