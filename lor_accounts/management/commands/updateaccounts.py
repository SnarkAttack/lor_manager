import json
from django.core.management.base import BaseCommand, CommandError
import os
import json
from lor_accounts.models import LorAccount
from django.conf import settings
from requests.exceptions import HTTPError
from time import sleep
from lor_manager import riot_watcher

class Command(BaseCommand):
    help = 'Updates any lor_accounts in the database that are missing data'

    def handle(self, *args, **options):

        accounts = LorAccount.objects.filter(game_name=None)

        for account in accounts:
            print(f"Updating account for puuid {account.puuid}")
            account_results = riot_watcher.account.by_puuid(region="americas", puuid=account.puuid)

            account.game_name = account_results['gameName']
            account.tag_line = account_results['tagLine']

            account.save()

            sleep(2)




        