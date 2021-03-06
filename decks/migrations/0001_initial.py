# Generated by Django 3.1.7 on 2021-03-22 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cards', '0002_card_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeckCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.card')),
            ],
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deck_code', models.CharField(max_length=64, unique=True)),
                ('champions', models.ManyToManyField(to='cards.Card')),
                ('deck_cards', models.ManyToManyField(to='decks.DeckCard')),
                ('regions', models.ManyToManyField(to='cards.Region')),
            ],
        ),
    ]
