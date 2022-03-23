from django.db import models

class FeedLink(models.Model):
    rss_link = models.URLField(unique=True)
