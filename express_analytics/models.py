import requests
from django.core.mail import send_mail
from django.db import models

from django.db.models import CharField, EmailField, TextField, IntegerField
from olx_ua_parser.settings import EMAIL_HOST_USER


class Report(models.Model):
    email = EmailField('Email', blank=False)
    url = CharField(max_length=255, blank=False)
    title = CharField(default='', max_length=255)
    pages_amount = IntegerField(default=0)
    weekly = TextField('')
    hourly = TextField('')

    def assemble_url(self):
        return 'https://olx.ua/{url}/'.format(url=self.url)

    def assemble_output_url(self):
        from django.urls import reverse
        from olx_ua_parser.settings import ABSOLUTE_URL
        print(ABSOLUTE_URL)
        return ABSOLUTE_URL + reverse('report_detail', args=[str(self.id)])

    def validate_url(self):
        if requests.get(self.assemble_url()).status_code == 200:
            return True
        return False

    def send_mail(self):
        subject = u'Новый отчет'
        message = u'Ваш отчет по странице "{title}" готов.' \
                  u'Вы можете посмотреть его здесь: {url}'.format(title=self.title, url=self.assemble_output_url())
        send_mail(subject, message, EMAIL_HOST_USER, [self.email])
