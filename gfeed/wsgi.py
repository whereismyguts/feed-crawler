"""
WSGI config for gfeed project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import atexit

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gfeed.settings")

application = get_wsgi_application()

from .crawler import CrawlManager
def exithandler():
    CrawlManager().stop()
atexit.register(exithandler)    
CrawlManager().start()






