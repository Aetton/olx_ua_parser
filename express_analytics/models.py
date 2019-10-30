import requests
from django.db import models

from django.db.models import CharField, EmailField, TextField, IntegerField


class Report(models.Model):
    email = EmailField('Email', blank=False)
    url = CharField(max_length=255, blank=False)
    title = CharField(max_length=255)
    pages_amount = IntegerField()
    weekly = TextField('')
    hourly = TextField('')

    @classmethod
    def assemble_url(self):
        return 'https://olx.ua/{url}/'.format(self.url)

    @classmethod
    def validate_url(self):
        if requests.get(self.assemble_url()).status_code == 200:
            return True
        return False
