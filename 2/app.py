from flask import Flask
import requests
import json
from collections import defaultdict
import pytz
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():

    result = {
      'status': 200,
      'message': ""
    }

    # idr2usd_rate = get_rate()
    json_users = []
    sensors = load_json_file()
    # print sensors

    tz = pytz.timezone('Asia/Jakarta')

    for x in sensors:
      x['date'] = datetime.utcfromtimestamp(x['timestamp']).isoformat()

    # if (len(json_users) > 0) & (len(salary) > 0):
    #   d = defaultdict(dict)
    #   for l in (json_users, salary):
    #     for elem in l:
    #       if ('salaryInIDR' in elem):
    #         if (idr2usd_rate is not None):
    #           elem['salaryInUSD'] = elem['salaryInIDR']*idr2usd_rate
    #         else:
    #           elem['salaryInUSD'] = None
    #       else:
    #         del elem['website']
    #         del elem['company']
    #       d[elem['id']].update(elem)

    #   result['data'] = d.values()

    result['data'] = sensors

    return json.dumps(result)

def load_json_file():
  raw_data = open('sensor_data.json',) 
  data = json.load(raw_data)['array']
  return data

def get_users():
  uri = "http://jsonplaceholder.typicode.com/users/"
  try:
    raw_users = requests.get(uri)
    if raw_users.status_code == 200:
      json_users = json.loads(raw_users.text)
      return json_users
    else:
      return []

  except requests.exceptions.RequestException as e:
    return []



def get_rate():
  uri = "https://free.currconv.com/api/v7/convert?q=IDR_USD&compact=ultra&apiKey=da8c1dc7a695fbaeffbc"
  try:
    raw_idr2usd_rate = requests.get(uri)

    if (raw_idr2usd_rate.status_code == 200):
      idr2usd_rate = raw_idr2usd_rate.text
      idr2usd_rate = json.loads(raw_idr2usd_rate.text)['IDR_USD']
      return idr2usd_rate
    else:
      return None

  except requests.exceptions.RequestException as e:
    return None


if __name__ == '__main__':
    app.run(debug=True)