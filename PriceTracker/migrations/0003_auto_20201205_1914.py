# Generated by Django 3.1.4 on 2020-12-05 13:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('PriceTracker', '0002_urls_exp_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urls',
            name='exp_price',
            field=models.TextField(default=100),
        ),
    ]
