from pip._internal.utils import logging

from express_analytics.models import Report
from olx_ua_parser.celery import app

@app.task
def parse_data_from_url(report_id):
    report = Report.objects.get(id=report_id)
    report.send_mail()
