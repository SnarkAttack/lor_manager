from django.db import models

class VocabTerm(models.Model):
    name = models.CharField(max_length=32)
    name_ref = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=1024)
    language = models.CharField(max_length=32)

class Keyword(models.Model):
    name = models.CharField(max_length=32)
    name_ref = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=1024)
    language = models.CharField(max_length=32)

class Region(models.Model):
    name = models.CharField(max_length=32)
    name_ref = models.CharField(max_length=32, unique=True)
    file_name = models.CharField(max_length=256, unique=True)
    abbreviation = models.CharField(max_length=8, unique=True)
    language = models.CharField(max_length=32)

class SpellSpeed(models.Model):
    name = models.CharField(max_length=32)
    name_ref = models.CharField(max_length=32, unique=True)
    language = models.CharField(max_length=32)

class Rarity(models.Model):
    name = models.CharField(max_length=32)
    name_ref = models.CharField(max_length=32, unique=True)
    language = models.CharField(max_length=32)

class Set(models.Model):
    name = models.CharField(max_length=32)
    name_ref = models.CharField(max_length=32, unique=True)
    file_name = models.CharField(max_length=256, unique=True)
    language = models.CharField(max_length=32)

class Card(models.Model):
    associated_cards = models.ManyToManyField("self", blank=True)
    asset_path = models.CharField(max_length=256)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    attack = models.IntegerField(null=True)
    cost = models.IntegerField(null=True)
    health = models.IntegerField(null=True)
    description = models.CharField(max_length=1024)
    description_raw = models.CharField(max_length=1024)
    level_up_description = models.CharField(max_length=1024)
    level_up_description_raw = models.CharField(max_length=1024)
    flavor_text = models.CharField(max_length=1024)
    artist_name = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    card_code = models.CharField(max_length=16, unique=True)
    keywords = models.ManyToManyField(Keyword, blank=True)
    spell_speed = models.ForeignKey(SpellSpeed, on_delete=models.CASCADE, null=True)
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    subtype = models.CharField(max_length=32)
    supertype = models.CharField(max_length=32)
    type = models.CharField(max_length=32)
    collectible = models.BooleanField()
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    language = models.CharField(max_length=32)

    class Meta:
        ordering = ('-supertype', 'cost', 'name')

    def get_img_abspath(self):
        return f'cards/lor_data/{self.set.name_ref.lower()}/{self.language}/img/cards/{self.asset_path}'

    @classmethod
    def get_collectible_cards(cls):
        return cls.objects.filter(collectible=True)


