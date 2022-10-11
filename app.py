from flask import Flask, request
from bs4 import BeautifulSoup
import requests as rq
import json
import git
import os
import sys
import logging

app = Flask(__name__)
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


@app.route('/api/v1/check_update')
def check_update():
    items_dict = {}
    url = 'https://www.muiv.ru/studentu/fakultety-i-kafedry/fakultet-it/raspisaniya/'
    soup = BeautifulSoup(rq.get(url).text, 'lxml')
    files_div = soup.find('div', class_='m-intext-docs')
    logging.info(files_div)

    for i, item in enumerate(files_div.find_all('div', class_='m-doc')):
        for n, par in enumerate(item.find_all('p')):
            logging.info(par)
        url = item.p.a['href']
        url_items = url.split('/')
        items_dict[f'doc{i}'] = {
            'url': f'https://www.muiv.ru{url}',
            'id': url_items[3],
            'fileName': url_items[4],
            'fileSize': item.p.text
        }

    return items_dict



@app.route('/api/v1/get/img/<string:file_name>', methods=['GET'])
def getImg(file_name):
    for root, _, files in os.walk('./UnivAPI/files/'):
        if file_name in files:
            return os.path.join(root, file_name)
    return 'None'

    # convert(file_name)


def convert(file_name):

    instructions = {
      'parts': [
        {
          'file': 'document'
        }
      ],
      'output': {
        'type': 'image',
        'format': 'png',
        'dpi': 500
      }
    }

    response = rq.request(
      'POST',
      'https://api.pspdfkit.com/build',
      headers = {
        'Authorization': 'Bearer pdf_live_qpcg2HFUbaP4u52RoRabxOb8DFxL5GMoxQyh4xGGMsq'
      },
      files = {
        'document': open(f'{file_name}.xls', 'rb')
      },
      data = {
        'instructions': json.dumps(instructions)
      },
      stream = True
    )

    if response.ok:
      with open('image.png', 'wb') as fd:
        for chunk in response.iter_content(chunk_size=8096):
          fd.write(chunk)
    else:
      print(response.text)

