# Generated by Django 3.1.7 on 2021-03-23 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_card_language'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ('-supertype', 'cost', 'name')},
        ),
    ]