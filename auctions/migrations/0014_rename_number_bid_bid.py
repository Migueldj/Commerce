# Generated by Django 3.2.2 on 2021-05-22 04:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_alter_bid_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='number',
            new_name='bid',
        ),
    ]