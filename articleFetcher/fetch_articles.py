from dateutil import parser
from feeder.models import FeedLink, Article
import feedparser
import ssl

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

def fetch_articles():

    feedlist = FeedLink.objects.values_list('rss_link', flat=True) 
    for feed in feedlist:
        feed = feedparser.parse(feed)

        for item in feed.entries:
            if not Article.objects.filter(title=item.title).exists():
                article = Article(
                    title=item.title,
                    description=item.description,
                    link=item.link,
                    tags=item.tags,
                )
                print(article)
                article.save()

