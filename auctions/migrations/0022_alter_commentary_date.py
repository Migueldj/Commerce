# Generated by Django 3.2.2 on 2021-06-09 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_alter_commentary_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentary',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
