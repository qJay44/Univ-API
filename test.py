import requests
import json
from sys import argv

instructions = {
  'parts': [
    {
      'file': 'document'
    }
  ],
  'output': {
    'type': 'image',
    'pages': { 'start': -1, 'end': -1 },
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
    'document': open(argv[0], 'rb')
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
  exit()
