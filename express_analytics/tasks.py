from grab import Grab
from pip._internal.utils import logging

from express_analytics.models import Report
from olx_ua_parser.celery import app

@app.task
def parse_data_from_url(report_id):
    report = Report.objects.get(id=report_id)
    report.pages_amount = get_pages_amount(report_id)
    report.save()
    report.send_mail()


def get_pages_amount(report_id):
    report = Report.objects.get(id=report_id)
    url = report.assemble_url()
    g = Grab(log_file='out.html')
    g.go(url)
    return int(g.doc.select("//*[@data-cy='page-link-last']").text())

