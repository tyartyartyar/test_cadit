from flask import Flask
import requests
import json
from collections import defaultdict

app = Flask(__name__)

@app.route('/')
def index():

    result = {
      'status': 200,
      'message': ""
    }

    json_users = get_users()
    idr2usd_rate = get_rate()
    salary = load_json_file()

    if (len(json_users) > 0) & (len(salary) > 0):
      d = defaultdict(dict)
      for l in (json_users, salary):
        for elem in l:
          if ('salaryInIDR' in elem):
            if (idr2usd_rate is not None):
              elem['salaryInUSD'] = elem['salaryInIDR']*idr2usd_rate
            else:
              elem['salaryInUSD'] = None
          else:
            del elem['website']
            del elem['company']
          d[elem['id']].update(elem)

      result['data'] = d.values()

    return json.dumps(result)

def load_json_file():
  raw_salary = open('salary_data.json',) 
  salary = json.load(raw_salary)['array']
  return salary

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