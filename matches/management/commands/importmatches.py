import json
from django.core.management.base import BaseCommand, CommandError
import os
import json
from matches.models import Match
from django.conf import settings
from riotwatcher import LorWatcher
from requests.exceptions import HTTPError
from time import sleep

class Command(BaseCommand):
    help = 'Prepares card data for loading into database'

    def handle(self, *args, **options):

        lor_watcher = LorWatcher(api_key=settings.RIOT_API_KEY)

        with open('match_ids.json', 'r') as f:
            match_ids = json.load(f)

        i = 0

        while i < len(match_ids):
            match_id = match_ids[i]
            try:
                match = Match.objects.get(match_id=match_id)
                i += 1
            except Match.DoesNotExist as e:
                print(f"Generating match for match id {match_id}")

                try:
                    match_results = lor_watcher.match.by_id(region="americas", match_id=match_id)
                    Match.create(match_results)
                    i += 1
                except HTTPError as e:
                    status_code = e.response.status_code
                    if status_code == 429:
                        print("Too many requests, waiting for 10 minutes")
                        sleep(600)
                    else:
                        print(f"Error code {status_code}")

                sleep(1)