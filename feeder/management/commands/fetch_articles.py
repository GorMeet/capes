from django.core.management.base import BaseCommand
from dateutil import parser
from feeder.models import FeedLink
import feedparser
import ssl
import json

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


def save_new_article(search):

    '''
    url_list = ['http://rss.cnn.com/rss/cnn_topstories.rss',
                'http://rss.cnn.com/rss/money_latest.rss',
                'http://rss.cnn.com/rss/cnn_tech.rss',
                'http://feeds.nytimes.com/nyt/rss/Technology',
                'http://www.wsj.com/xml/rss/3_7455.xml',
                'https://indianexpress.com/feed/',      
                'https://www.theguardian.com/help/feeds',
                'https://telegraph.co.uk/rss.xml',
               ]
    '''
    url_list = FeedLink.objects.values_list('rss_link', flat=True) 

    search_result = []
    search = search.lower()
    for url in url_list:

        current = feedparser.parse(url)
        if len(current.entries) > 5:
          #print(f"{len(current.entries)} -> {url}")
            for post in current.entries:
                title = post.title.lower()
                tags = []
                if 'description' in post:
                    description = post.description.lower()
                if 'tags' in post:
                    for tag in post['tags']:
                        if 'term' in tag:
                            tags = tag.term.lower()
                        else:
                            tags = tag.lower()
                if search in tags or search in title or search in description:
                    search_result.append({'title':post.title, 'link':post.link})
    return search_result[:15]
    '''
    feedlist = FeedLink.objects.values_list('rss_link', flat=True) 
    for feed in feedlist:
        feed = feedparser.parse(feed)
        article_title = feed.channel.title

        for item in feed.entries:
            if not Article.objects.filter(puid=item.guid).exists():
                article = Article(
                    title=item.title,
                    description=item.description,
                    pub_date=parser.parse(item.published),
                    link=item.link,
                    publication_name=article_title,
                    puid=item.guid,
                )
                article.save()
    '''


class Command(BaseCommand):
    def add_arguments(self , parser):
        parser.add_argument('--search', action='append', type=str)
    def handle(self,  *args, **options):
        return json.dumps(save_new_article(options['search']))
