import json
import locale
import time
from datetime import datetime, timedelta

from celery.utils.log import get_task_logger
from grab import Grab, GrabTimeoutError
from weblib.error import DataNotFound

from express_analytics.models import Report
from olx_ua_parser.celery import app

@app.task
def parse_data_from_url(report_id):
    logging = get_task_logger('parse')
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8') #Пока не проверял, как работает с локалью сам Джанго, потом протестирую
    report = Report.objects.get(id=report_id)
    report.pages_amount = get_pages_amount(report_id)
    report.title = get_title(report_id)
    weekly = json.loads(report.weekly)
    hourly = json.loads(report.hourly)
    for page in range(1, report.pages_amount+1):
        url = report.assemble_url() + '?page={page}'.format(page=page)
        g = Grab(log_file='page_out.html')
        try:
            g.go(url)
        except GrabTimeoutError:
            continue
        page_urls = g.doc.select('//*[@id="offers_table"]//*[@data-cy="listing-ad-title"]/@href').text_list()
        for page_url in page_urls:
            dt = get_page_datetime(page_url)
            if dt:
                hourly[str(dt.hour)] += 1
                weekly[dt.strftime('%A')] += 1
    report.hourly = json.dumps(hourly)
    report.weekly = json.dumps(weekly)
    report.save()
    report.send_mail()


def get_pages_amount(report_id):
    report = Report.objects.get(id=report_id)
    url = report.assemble_url()
    g = Grab(log_file='index_out.html')
    g.go(url)
    return int(g.doc.select("//*[@data-cy='page-link-last']").text())

def get_title(report_id):
    report = Report.objects.get(id=report_id)
    url = report.assemble_url()
    g = Grab(log_file='index_out.html')
    g.go(url)
    return g.doc.select('.//title').text()

def get_page_datetime(url):
    logging = get_task_logger('page')
    try:
        g = Grab(log_file='offer_out.html')
        g.go(url)
        dt_format = '%H:%M, %d %B %Y'
        dt = g.doc.rex_text(r'в (\d{2}:\d{2}, .*?),')
        # Добавляем 5 минут, чтобы объявление в 23:55 или 23:57 считалось как объявление следующего часа
        return datetime.strptime(dt, dt_format) + timedelta(minutes=5)
    except GrabTimeoutError:
        return False
    except DataNotFound:
        # Странная ошибка, возникает на самой обычной странице
        return False
    except Exception as e:
        logging.error(e.args)


