from .celery import app as celery_app
from riotwatcher import LorWatcher, RiotWatcher
from django.conf import settings

__all__ = ('celery_app',)

lor_watcher = LorWatcher(api_key=settings.RIOT_API_KEY)
riot_watcher = RiotWatcher(api_key=settings.RIOT_API_KEY)