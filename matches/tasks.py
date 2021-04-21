from celery import shared_task
from matches.models import Match
from django.conf import settings
from requests.exceptions import HTTPError
from lor_manager import lor_watcher

puuid = "IkY72FK0gy4Bs3X70zMs4m69xJGA54EI8CNkWHofuw_WTHhRVs72MjsW3RYhp0TJJXGD2LyKA-pBBQ"

@shared_task
def monitor_player_games():

        try:
            match_ids = lor_watcher.match.by_puuid(region="americas", puuid=puuid)

            for match_id in match_ids:

                try: 
                    match = Match.objects.get(match_id=match_id)
                except Match.DoesNotExist as e:
                    print(f"Generating match for match id {match_id}")

                    match_results = lor_watcher.match.by_id(region="americas", match_id=match_id)

                    Match.create(match_results)
        except HTTPError as e:
            status_code = e.response.status_code
            if status_code == 403:
                print("API Key invalid!")
            else:
                print(f"API request errored with status code {status_code}")