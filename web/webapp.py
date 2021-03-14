from flask import Flask, redirect, url_for, request, render_template, Response, stream_with_context
import ancv_html_scraper as ancv
import logging
from logging.handlers import RotatingFileHandler
from database.db import initialize_db, drop_db
from database.models import Restaurants
import json
from pymongo import MongoClient

app = Flask(__name__)

# Init mongodb
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://my_db:27017'
}
initialize_db(app)

@app.route('/')
def index():
    app.logger.info('User: ' + request.environ['REMOTE_ADDR'])
    return render_template('home.html')

@app.route('/success/<city_name>')
def success(city_name):
    # Check if the city is already present in the database
    response = get_restaurant_by_city(city_name)

    if response != None and len(response.get_data(as_text=True)) > 0:
        body = str(response.get_json())
        body = body.replace("'", "\"")
        resto = Restaurants.from_json(body)
        if resto != None:
            return render_template("results.html", result = resto.restaurants, city=city_name)

    result = ancv.restoLookup(city_name)

    if result != None:
        mongoItem = Restaurants(city=city_name, restaurants=result)
        mongoItem.save()

    return render_template("results.html", result = result, city=city_name)

@app.route('/home',methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        city = request.form['nm']
        return redirect(url_for('success', city_name=city.lower()))
    else:
        city = request.args.get('nm')
        return redirect(url_for('success', city_name=city.lower()))

# MONGO RESTFUL API
@app.route('/restaurants/<id>')
def get_restaurant(id):
    resto = Restaurants.objects.get(id=id).to_json()
    return Response(resto, mimetype="application/json", status=200)

@app.route('/restaurants/city/<city>')
def get_restaurant_by_city(city):
    if Restaurants.objects.count() == 0 or Restaurants.objects(city=city).count() == 0:
        if request.method == 'GET':
            return Response([], mimetype="application/json", status=200)
        else:
            return None
    else:
        resto = Restaurants.objects.get(city=city).to_json()
        return Response(resto, mimetype="application/json", status=200)

@app.route('/restaurants')
def get_restaurants():
    restos = Restaurants.objects().to_json()
    return Response(restos, mimetype="application/json", status=200)

@app.route('/restaurants', methods=['POST'])
def add_restaurant():
    body = request.get_json()
    resto = Restaurants(**body).save()
    id = resto.id
    return {'id': str(id)}, 200

@app.route('/restaurants/<id>', methods=['PUT'])
def update_resto(id):
    body = request.get_json()
    Restaurants.objects.get(id=id).update(**body)
    return '', 200

@app.route('/restaurants/<id>', methods=['DELETE'])
def delete_resto(id):
    Restaurants.objects.get(id=id).delete()
    return '', 200

@app.route('/truncate', methods=['DELETE'])
def delete_all_resto():
    drop_db(app)    
    return '', 200

if __name__ == '__main__':
    handler = RotatingFileHandler('logfile.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    handler.setFormatter("[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")
    app.logger.addHandler(handler)
    app.run(debug=True, host ='0.0.0.0')