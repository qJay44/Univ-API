from flask import Flask, request
from bs4 import BeautifulSoup
from selenium import webdriver
from werkzeug.exceptions import RequestTimeout
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests as rq
import json
import git
import os
import logging
import uuid

app = Flask(__name__)
app.config['TRAP_HTTP_EXCEPTIONS'] = True
logging.basicConfig(filename="info.log", level=logging.INFO)


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('./UnivAPI')
        origin = repo.remotes.origin

        origin.pull()

        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


@app.route('/api/v1/check_schedule')
def check_update():
    webData = getWebData()
    dbData = ...
    return webData


@app.route('/api/v1/get/img/<string:file_name>', methods=['GET'])
def getImg(file_name):
    for root, _, files in os.walk('./UnivAPI/files/'):
        if file_name in files:
            return os.path.join(root, file_name)
    return 'None'

    # convert(file_name)


@app.errorhandler(Exception)
def hadle_error(e):
    if e.code == 504:
        return 'Page load timeout'



def getWebData():
    """
    FIXME: Page loading problem

    forms[0] = Очная
    forms[1] = Заочная
    forms[2] = Очно-заочная

    """
    forms = [
        '\u041e\u0447\u043d\u0430\u044f',
        '\u0417\u0430\u043e\u0447\u043d\u0430\u044f',
        '\u041e\u0447\u043d\u043e-\u0437\u0430\u043e\u0447\u043d\u0430\u044f'
    ]
    url = 'https://www.muiv.ru/studentu/fakultety-i-kafedry/fakultet-it/raspisaniya/'

    source = tryToLoadPage(url)
    soup = BeautifulSoup(source, 'lxml')
    files_div = soup.find('div', class_='m-intext-docs')
    items_dict = {}

    for item in files_div.find_all('div', class_='m-doc'):
        file_props = [p for p in item.find_all('p')]
        url = file_props[0].a['href']
        url_items = url.split('/')
        original_name = file_props[0].a.text
        eduForm = [f for f in forms if f in original_name][0]
        items_dict[str(uuid.uuid4())] = {
            'eduForm': eduForm,
            'url': f'https://www.muiv.ru{url}',
            'id': url_items[3],
            'fileName': url_items[4],
            'fileSize': file_props[1].text.split(' ')[1],
            'updateTime': file_props[2].text[-10:],
            'origName': original_name,
        }

    return items_dict


def tryToLoadPage(url):
    url_request = rq.get(url).text
    if 'https://static.stormwall.pro/ajax-loader.gif' in url_request:
        try:
            options = Options()
            options.headless = True
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'm-intext-docs')))
        except TimeoutException:
            logging.error('Page loading timeout exception')
            raise RequestTimeout()
        finally:
            return driver.page_source

    return url_request


def convert(file_name):
    ...

