# Generated by Django 3.1.7 on 2021-03-21 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('name_ref', models.CharField(max_length=32, unique=True)),
                ('description', models.CharField(max_length=1024)),
                ('language', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Rarity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('name_ref', models.CharField(max_length=32, unique=True)),
                ('language', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('name_ref', models.CharField(max_length=32, unique=True)),
                ('file_name', models.CharField(max_length=256, unique=True)),
                ('abbreviation', models.CharField(max_length=8, unique=True)),
                ('language', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('name_ref', models.CharField(max_length=32, unique=True)),
                ('file_name', models.CharField(max_length=256, unique=True)),
                ('language', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='SpellSpeed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('name_ref', models.CharField(max_length=32, unique=True)),
                ('language', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='VocabTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('name_ref', models.CharField(max_length=32, unique=True)),
                ('description', models.CharField(max_length=1024)),
                ('language', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_path', models.CharField(max_length=256)),
                ('attack', models.IntegerField(null=True)),
                ('cost', models.IntegerField(null=True)),
                ('health', models.IntegerField(null=True)),
                ('description', models.CharField(max_length=1024)),
                ('description_raw', models.CharField(max_length=1024)),
                ('level_up_description', models.CharField(max_length=1024)),
                ('level_up_description_raw', models.CharField(max_length=1024)),
                ('flavor_text', models.CharField(max_length=1024)),
                ('artist_name', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=128)),
                ('card_code', models.CharField(max_length=16, unique=True)),
                ('subtype', models.CharField(max_length=32)),
                ('supertype', models.CharField(max_length=32)),
                ('type', models.CharField(max_length=32)),
                ('collectible', models.BooleanField()),
                ('associated_cards', models.ManyToManyField(blank=True, related_name='_card_associated_cards_+', to='cards.Card')),
                ('keywords', models.ManyToManyField(blank=True, to='cards.Keyword')),
                ('rarity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.rarity')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.region')),
                ('set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.set')),
                ('spell_speed', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cards.spellspeed')),
            ],
        ),
    ]
