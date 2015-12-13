from flask import Flask, render_template, request, redirect
from pprint import pformat

import pandas as pd

from bokeh.plotting import figure
from bokeh.embed import components

import requests

import datetime

app = Flask(__name__)
app.debug = True

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/stock')
def stock():
  start_d = str(datetime.date.today() - datetime.timedelta(days=30))
  end_d = str(datetime.date.today())
  ticker = request.args.get('ticker')
  r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/{}.json?&start_date={}&end_date={}&column_index=4'.format(ticker,start_d,end_d))
  data = r.json()['dataset']['data']
  df = pd.DataFrame(data)
  p = figure(title="{} chart".format(ticker), x_axis_type='datetime')
  p.circle(pd.to_datetime(df[0]),df[1])
  script,div = components(p)
  # raw = r.text()
  
  return render_template('stock.html',raw=data,script=script,div=div,ticker=ticker)

if __name__ == '__main__':
  app.run(port=33507)
