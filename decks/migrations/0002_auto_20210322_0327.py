# Generated by Django 3.1.7 on 2021-03-22 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='deck_code',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
