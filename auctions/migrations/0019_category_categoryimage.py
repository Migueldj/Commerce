# Generated by Django 3.2.2 on 2021-06-08 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_listing_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='categoryImage',
            field=models.URLField(null=True),
        ),
    ]
