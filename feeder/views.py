from django.views.generic import ListView, CreateView
from django.shortcuts import render
from django.core.management import call_command
import feedparser
from django.forms.models import model_to_dict
from .models import FeedLink, Article
from .forms import AddFeedForm
from io import StringIO
import json

def home(request):
    return render(request, 'base.html')

def fetchfeed(request):
    context = {}
    context['articles'] = []
    searchterm = request.POST.get("searchterm")
    articles_list = Article.objects.values()

    for article in articles_list:
        if searchterm in article['title'].lower() or searchterm in article['description'].lower() :
            for tag in article['tags']:
                if searchterm in tag:
                    context['articles'].append(article)
            context['articles'].append(article)
    
    posts = len(context["articles"])
    if posts == 0:
        out = StringIO()
        if not searchterm:
            searchterm = "news"
        call_command('fetch_articles', search=searchterm, stdout=out)
        context["articles"] = json.loads(out.getvalue())
    return render(request, 'fetch.html', {'articles':context["articles"], 'searchterm':searchterm})

class AddFeed(CreateView):
    model = FeedLink
    form_class = AddFeedForm
    success_url = '/'

def savefeed(request):
    context = {}
    out = StringIO()
    searchterm = request.POST.get("searchterm")
    if not searchterm:
        searchterm = "news"
    call_command('fetch_articles', search=searchterm, stdout=out)
    context["articles"] = json.loads(out.getvalue())
    for item in context['articles']:
        tags=[]
        if 'description' in item:
            description = item['description']
        if 'tags' in item:
            for tag in item['tags']:
                if 'term' in tag:
                    tags.append(tag['term'].lower())
                else:
                    tags.append(tag.lower())
        article = Article(
            title=item['title'],
            link=item['link'],
            tags=tags,
            description=description
        )
        article.save()
    articles = model_to_dict(Article)
    return render(request, 'send.html', {'articles':articles})
