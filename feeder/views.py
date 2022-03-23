from django.shortcuts import render
from django.core.management import call_command
import feedparser
from io import StringIO
import json

def home(request):
    return render(request, 'base.html')

def fetchfeed(request):
    context = {}
    out = StringIO()
    searchterm = request.POST.get("searchterm")
    if not searchterm:
        searchterm = "news"
    call_command('fetch_articles', search=searchterm, stdout=out)
    context["articles"] = json.loads(out.getvalue())
    return render(request, 'fetch.html', {'articles':context["articles"]})
