from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.shortcuts import render
from .models import ScheduledMail
from .forms import MailForm
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template import loader

from pathlib import Path
from feeder.views import get_list


class AddMailView(LoginRequiredMixin, CreateView):
    model = ScheduledMail
    form_class = MailForm
    success_url = "/"
    template_name = "mail/add.html"

    def get_initial(self):
        article_list = self.request.session.get("articles")
        BASE_DIR = Path(__file__).resolve().parent.parent
        html_message = loader.render_to_string(
            Path(BASE_DIR, "templates/mail/mail_template.html"),
            {"articles": article_list},
        )
        print(html_message)
        articles = []
        for article in article_list:
            articles.append(article["link"])

        return {"body": html_message}

    def form_valid(self, form):
        form.instance.sender = self.request.user.email
        return super(AddMailView, self).form_valid(form)
