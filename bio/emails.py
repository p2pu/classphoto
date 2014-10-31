from django.conf import settings
from django.template.loader import render_to_string
import json
from mailgun import api as mailgun_api

def send_user_link( email, sequence, key ):
    context = {
        'email': email,
        'sequence': sequence,
        'key': key,
        'mooc_title': settings.MOOC_TITLE,
        'mooc_domain': settings.MOOC_DOMAIN
    }
    subject = render_to_string('bio/emails/user-link-subject.txt', context).strip()
    text_body = render_to_string('bio/emails/user-link.txt', context).strip()
    html_body = render_to_string('bio/emails/user-link.html', context).strip()
    mailgun_api.send_email(email, settings.DEFAULT_FROM_EMAIL, subject, text_body, html_body, tags=['user_link'])
