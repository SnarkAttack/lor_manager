from django.db import models
from cards.models import Card, Region
from lor_deckcodes import LoRDeck

class DeckCard(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @classmethod
    def get_or_create(cls, card_code_and_count):
        quantity, card_code = card_code_and_count.split(':')
        card = Card.objects.get(card_code=card_code)
        deck_card, created = DeckCard.objects.get_or_create(card=card, quantity=quantity)
        return deck_card

class Deck(models.Model):
    deck_code = models.CharField(max_length=128, unique=True)
    regions = models.ManyToManyField(Region)
    deck_cards = models.ManyToManyField(DeckCard)
    champions = models.ManyToManyField(Card)

    def add_deck_fields(self, deck_code):
        deck_from_code = LoRDeck.from_deckcode(deck_code)

        deck_cards = [DeckCard.get_or_create(ccac) for ccac in list(deck_from_code)]
        regions = list(set(deck_card.card.region for deck_card in deck_cards))
        champions = [deck_card.card for deck_card in deck_cards if deck_card.card.supertype == "Champion"]

        self.regions.add(*regions)
        self.deck_cards.add(*deck_cards)
        self.champions.add(*champions)

    @classmethod
    def get_or_create(cls, deck_code):

        deck, created = Deck.objects.get_or_create(deck_code=deck_code)

        if created:
            deck.add_deck_fields(deck_code)

        return deck

