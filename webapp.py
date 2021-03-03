from flask import Flask, redirect, url_for, request, render_template, Response, stream_with_context
import ancv_html_scraper as ancv
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

@app.route('/')
def index():
    app.logger.info('User: ' + request.environ['REMOTE_ADDR'])
    return render_template('home.html')

@app.route('/success/<city_name>')
def success(city_name):
    result = ancv.restoLookup(city_name)
    return render_template("results.html", result = result, city=city_name)

@app.route('/home',methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        city = request.form['nm']
        return redirect(url_for('success',city_name = city))
    else:
        city = request.args.get('nm')
        return redirect(url_for('success',city_name = city))

if __name__ == '__main__':
    handler = RotatingFileHandler('logfile.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    handler.setFormatter("[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")
    app.logger.addHandler(handler)
    app.run(debug=True, host ='0.0.0.0')