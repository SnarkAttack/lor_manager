from django.db import models
from decks.models import Deck
from cards.models import Card
from lor_manager import riot_watcher

# Create your models here.

class LorAccount(models.Model):
    puuid = models.CharField(max_length=128, unique=True)
    game_name = models.CharField(max_length=32, null=True)
    tag_line = models.CharField(max_length=32, null=True)

    @classmethod
    def get_or_create(cls, puuid):

        try: 
            account = LorAccount.objects.get(puuid=puuid)
        except LorAccount.DoesNotExist:
            account_results = riot_watcher.account.by_puuid(region="americas", puuid=puuid)
            account = LorAccount(puuid=account_results['puuid'], game_name=account_results['gameName'], tag_line=account_results['tagLine'])
            account.save()

        return account

class AccountDeck(models.Model):
    account = models.ForeignKey(LorAccount, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)

    @classmethod
    def get_or_create(cls, puuid, deck_code):

        account = LorAccount.get_or_create(puuid=puuid)
        deck = Deck.get_or_create(deck_code=deck_code)

        account_deck, _ = AccountDeck.objects.get_or_create(account=account, deck=deck)

        return account_deck