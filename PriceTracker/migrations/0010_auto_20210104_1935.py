# Generated by Django 3.1.4 on 2021-01-04 14:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('PriceTracker', '0009_urlstotrack_sentemail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='urlstotrack',
            old_name='sentEmail',
            new_name='isEmailSent',
        ),
    ]
