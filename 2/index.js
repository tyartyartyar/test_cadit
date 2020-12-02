const express = require('express')
const app = express()
const port = process.env.PORT || 1234
const fs = require('fs');

const aggrThis = (arrOfObj, key) => {
  let res = arrOfObj.reduce((r, a) => {
    r[a[key]] = [...(r[a[key]] || []), a];
    return r;
  }, {})

  return res;
}

const minmax = (arrOfObj, key, minormax) => {
  return Math[minormax].apply(
    Math,
    arrOfObj.map(function (o) {
      return o[key];
    })
  );
}

const avg = (arrOfObj, key) => {
  return arrOfObj.reduce((r, a) => r + a[key], 0) / arrOfObj.length;
}

const median = (arrOfObj, key) => {
  let rawData = arrOfObj.map((e) => e[key]);

  rawData.sort(function (a, b) {
    return a - b;
  });

  let lowMiddle = Math.floor((rawData.length - 1) / 2);
  let highMiddle = Math.ceil((rawData.length - 1) / 2);
  let median = (rawData[lowMiddle] + rawData[highMiddle]) / 2;

  return median;
};

const formRes = (arr, key) => {
  return {
    min: minmax(arr, key, "min"),
    max: minmax(arr, key, "max"),
    avg: avg(arr, key),
    median: median(arr, key)
  }
}

app.get('/', (req, res) => {
  let result = {
    status: 200,
    message: ""
  }
  
  let rawdata = fs.readFileSync(__dirname + '/sensor_data.json');
  let data = JSON.parse(rawdata);
  data.array.map(e => e['date'] = new Date(e.timestamp).toDateString());

  let aggr = aggrThis(data.array, 'roomArea')
  Object.keys(aggr).map(e => aggr[e] = aggrThis(aggr[e], 'date'))

  let resp = {}

  resp['humidity'] = formRes(data.array, 'humidity')
  resp['temperature'] = formRes(data.array, 'temperature')

  result['data_aggregated'] = aggr
  result['data'] = resp
  res.send(result)
})

app.listen(port, () => {
  console.log(`Running at http://localhost:${port}`)
})
