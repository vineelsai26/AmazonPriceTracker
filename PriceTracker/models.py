from django.db import models


class UrlsToTrack(models.Model):
    username = models.TextField()
    email = models.TextField(default="vineelsai26@gmail.com")
    url = models.TextField()
    isEmailSent = models.BooleanField(default=False)
    exp_price = models.TextField(default=100)
