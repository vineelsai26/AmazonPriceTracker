# Generated by Django 3.1.4 on 2020-12-05 13:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('PriceTracker', '0003_auto_20201205_1914'),
    ]

    operations = [
        migrations.RenameField(
            model_name='urls',
            old_name='user',
            new_name='username',
        ),
    ]
