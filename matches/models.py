from django.db import models
from dateutil import tz
from dateutil.parser import isoparse
from lor_accounts.models import LorAccount, AccountDeck
from decks.models import Deck

# Create your models here.

class MatchPlayer(models.Model):
    account = models.ForeignKey(LorAccount, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    game_outcome = models.CharField(max_length=8)
    order_of_play = models.IntegerField()

    @classmethod
    def create(cls, player_details):
        account = LorAccount.get_or_create(puuid=player_details['puuid'])

        # Create an account deck to link this account to having used this deck, but
        # when it comes time to save the values only use the deck
        account_deck = AccountDeck.get_or_create(player_details['puuid'], player_details['deck_code'])

        match_player, _ = MatchPlayer.objects.get_or_create(
            account=account,
            deck=account_deck.deck,
            game_outcome=player_details['game_outcome'],
            order_of_play=player_details['order_of_play']
        )

        return match_player


class Match(models.Model):
    match_id = models.CharField(max_length=128)
    players = models.ManyToManyField(MatchPlayer)
    game_mode = models.CharField(max_length=32)
    game_type = models.CharField(max_length=32)
    game_start_time = models.DateTimeField()
    game_version = models.CharField(max_length=32)
    turn_count = models.IntegerField()


    @classmethod
    def create(cls, match_details):
        match_players = [MatchPlayer.create(player_details) for player_details in match_details['info']['players']]

        match, created = Match.objects.get_or_create(
            match_id=match_details['metadata']['match_id'],
            game_mode=match_details['info']['game_mode'],
            game_type=match_details['info']['game_type'],
            game_start_time=isoparse(match_details['info']['game_start_time_utc']),
            game_version=match_details['info']['game_version'],
            turn_count=match_details['info']['total_turn_count'],
        )

        if created:
            match.players.add(*match_players)

        return match