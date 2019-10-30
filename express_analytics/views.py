from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from express_analytics.models import Report


class RequestView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        report = Report(email=request.POST.get('email'), url=request.POST.get('url'))
        if not report.validate_url():
            messages.add_message(self.request, messages.ERROR, 'Некорректный URL')
        else:
            #Логика
            messages.add_message(self.request, messages.ERROR, 'Собираю статистику по {url} <br/> \
Ждите письма на {email}'.format(url=report.url, email=report.email))
        return redirect('request')
