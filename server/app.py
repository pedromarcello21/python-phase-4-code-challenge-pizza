#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os
# from flask_cors import CORS



BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

####################### Restaurants #######################

@app.get('/restaurants')
def get_restaurants():
    try:
        all_restuarants = Restaurant.query.all()
        return [restaurant.to_dict() for restaurant in all_restuarants], 200

    except:
        return {'error':'invalid root'}, 404



    
@app.get('/restaurants/<int:id>')
def get_restaurant(id):
    found_restaurant = Restaurant.query.where(Restaurant.id == id).first()
    if found_restaurant:
        return found_restaurant.to_dict(), 200
    else:
        return {'error':'Restaurant not found'}, 404
    
    
    
@app.delete('/restaurants/<int:id>')
def delete_restaurant(id):
    found_restaurant = Restaurant.query.where(Restaurant.id == id).first()
    if found_restaurant:
        db.session.delete(found_restaurant)
        db.session.commit()
        return {}, 204
    else:
        {'error':'Restaurant not found'}


####################### Pizzas #######################
@app.get('/pizzas')
def get_pizzas():
    all_pizzas = Pizza.query.all()
    return [pizza.to_dict() for pizza in all_pizzas], 200

####################### restaurant_pizzas #######################

@app.post('/restaurant_pizzas')
def add_restaurant_pizza():
    data = request.json
    try:
        new_restaurant_pizza = RestaurantPizza(price=data['price'], pizza_id=data['pizza_id'], restaurant_id=data['restaurant_id'])
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        return new_restaurant_pizza.to_dict(), 201
    except:
        return {'errors':["validation errors"]}, 400



if __name__ == "__main__":
    app.run(port=5555, debug=True)
