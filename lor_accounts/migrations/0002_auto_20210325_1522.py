# Generated by Django 3.1.7 on 2021-03-25 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lor_accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loraccount',
            old_name='username',
            new_name='game_name',
        ),
        migrations.AddField(
            model_name='loraccount',
            name='tag_line',
            field=models.CharField(max_length=32, null=True),
        ),
    ]