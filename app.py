from firebase_handler import FirebaseHandler
from werkzeug.exceptions import RequestTimeout
from univ_parser import UnivParser
from flask import Flask, request
import git
import os
import logging

app = Flask(__name__)
app.config['TRAP_HTTP_EXCEPTIONS'] = True
logging.basicConfig(filename="info.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


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
def check_schedule():
    webData = UnivParser().getWebData()
    db = FirebaseHandler()
    # for doc in webData.keys():
    #     db.addData('files', doc, webData[doc])

    logging.info(db.readData('files'))


    return db.readData('files')


@app.route('/api/v1/get/img/<string:file_name>', methods=['GET'])
def getImg(file_name):
    for root, _, files in os.walk('./UnivAPI/files/'):
        if file_name in files:
            return os.path.join(root, file_name)
    return 'None'

    # convert(file_name)


@app.errorhandler(RequestTimeout)
def hadle_error(e):
    if e.code == 504:
        return 'Page load timeout'


def convert(file_name):
    ...

