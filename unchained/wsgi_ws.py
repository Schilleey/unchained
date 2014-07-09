import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unchained.settings_production")
from ws4redis.uwsgi_runserver import uWSGIWebsocketServer
application = uWSGIWebsocketServer()