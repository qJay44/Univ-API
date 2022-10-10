from flask import Flask, request
import requests
import json
import git
import os

app = Flask(__name__)

@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('https://github.com/qJay44/Univ-API')
        origin = repo.remotes.origin

        origin.pull()

        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


@app.route('/api/v1/getImg/<file_name>', method=['GET'])
def getImg(file_name):
    for root, dirs, files in os.walk('/home/qJay44/mysite/files/'):
        if file_name in files:
            return os.path.join(root, file_name)

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

    response = requests.request(
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

