from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.html import strip_tags

from pathlib import Path
import smtplib, ssl

from django.core.mail import send_mail
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(sender_email, reciever_email, password, message, port):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, reciever_email, message.as_string())


def schedule_mail(context):
    send_time = context["send_time"]
    port = context["port"]
    sender_email = context["from"]
    reciever_email = context["to"]
    password = context["user_pswd"]
    article_list = context["articles"]
    subject = context["subject"]

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = reciever_email
    message["Subject"] = subject

    BASE_DIR = Path(__file__).resolve().parent.parent
    html_message = loader.render_to_string(
        Path(BASE_DIR, "templates/mail/mail_template.html"),
        {"articles": article_list},
    )
    text_content = strip_tags(html_message)
    body = MIMEText(article_list, "html")

    message.attach(body)
    from datetime import datetime
    from articleFetcher import schedule_mail
    from apscheduler.schedulers.blocking import BlockingScheduler

    scheduler = BlockingScheduler()
    scheduler.add_job(
        send_mail,
        "date",
        run_date=send_time,
        args=[sender_email, reciever_email, password, message, port],
    )
    scheduler.start()
