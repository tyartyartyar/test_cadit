const express = require("express");
const app = express();
const port = process.env.PORT || 1234;
const fs = require("fs");

const writeToJson = () => {
  let data = {
    Time: new Date().toISOString(),
    Value: (Math.random() * (0.0 - 100.0) + 0.02).toFixed(4),
  };

  let rawdata = fs.readFileSync(__dirname + "/sensors_data_new.json");

  let existing_data = JSON.parse(rawdata);
  console.log("🚀 ~ file: index.js ~ line 19 ~ existing_data", existing_data);
  existing_data.push(data);
  var data_string = JSON.stringify(existing_data);
  fs.writeFileSync("sensors_data_new.json", [data_string]);
};

app.get("/", (req, res) => {
  res.statusCode = 200;
  res.setHeader("Content-type", "application/csv");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.type("text/plain");

  let rawdata = fs.readFileSync(__dirname + "/sensors_data_new.json");
  let data = JSON.parse(rawdata);

  res.write("Time,Value\n");
  data.map((e) => {
    res.write(`${e.Time},${e.Value}\n`);
  });

  res.end();
});

setInterval(() => {
  writeToJson();
}, 120000);

app.listen(port, () => {
  console.log(`Running at http://localhost:${port}`);
});
