from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import ScheduledMail
from .forms import MailForm
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.html import strip_tags
from articleFetcher import schedule_mail

from pathlib import Path
from feeder.views import get_list
import smtplib, ssl

from django.core.mail import send_mail
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
        return {"body": html_message}

    def form_valid(self, form):

        form.instance.sender = self.request.user.email
        article_list = self.request.session.get("articles")
        context = {}
        context["from"] = self.request.user.email
        context["to"] = ",".join(form.instance.recipients_list)
        context["subject"] = form.instance.subject
        context["user_pswd"] = self.request.user.gapps_key
        context["port"] = 465
        context["send_time"] = form.instance.send_on
        context["articles"] = form.instance.body
        from articleFetcher import schedule_mail

        schedule_mail.schedule_mail(context)

        """
        BASE_DIR = Path(__file__).resolve().parent.parent
        html_message = loader.render_to_string(
            Path(BASE_DIR, "templates/mail/mail_template.html"),
            {"articles": article_list},
        )
        text_content = strip_tags(html_message)
        body = MIMEText(body, "html")

        message.attach(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(message["From"], message["To"], message.as_string())
        """
        return super(AddMailView, self).form_valid(form)
