# Generated by Django 3.2.2 on 2021-05-21 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20210521_1432'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='comments',
        ),
        migrations.AddField(
            model_name='commentary',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Comments', to='auctions.listing'),
        ),
    ]
