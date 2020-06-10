from flask import Flask, render_template, jsonify, request, Blueprint
from models import db, Bottle
from flask_jwt_extended import (
    jwt_required
)
route_bottles = Blueprint('route_bottles', __name__)
@route_bottles.route('/bottles', methods=['POST'])
@route_bottles.route('/bottles/<int:id>', methods=['DELETE'])
@route_bottles.route('/bottles/<int:id>', methods=['PUT'])
@jwt_required
def bottles(id=None):
    if request.method == 'POST':
        country = request.json.get('country')
        country_esp = request.json.get('country_esp')
        image = request.json.get('image')
        category_id = request.json.get('category_id')
        if not country:
            return jsonify({"error":"Country is required"}), 422
        if not country_esp:
            return jsonify({"error":"Country_esp is required"}), 422
        if not image:
            return jsonify({"error":"Image is required"}), 422
        if not category_id:
            return jsonify({"error":"Category is required"}), 422
        bottle = Bottle()
        bottle.country = country
        bottle.country_esp = country_esp
        bottle.image = image
        bottle.category_id = category_id
        db.session.add(bottle)
        db.session.commit()
        return jsonify(bottle.serialize()), 201

    if request.method == 'PUT':
        bottle = Bottle.query.get(id)
        bottle.country_esp = request.json.get('country_esp')
        db.session.commit()
        return jsonify(bottle.serialize()), 200

    if request.method == 'DELETE':
        bottle = Bottle.query.get(id)
        db.session.delete(bottle)
        db.session.commit()
        return jsonify({"success":"Deleted"}), 200

@route_bottles.route('/bottles/<int:id>', methods=['GET'])
@route_bottles.route('/bottles/category/<int:category_id>/<int:boolean>', methods=['GET'])        
def freebottles(id=None, category_id=None, boolean=1):
    if request.method == 'GET':
        if id is not None:
            bottle = Bottle.query.get(id)
            if bottle:
                return jsonify(bottle.serialize()), 200
            else:
                return jsonify({"error":"Not Found"}), 404
        elif category_id is not None:
            #Condition for show all the bootles in the route category_id
            if boolean is 1:
                bottles = Bottle.query.filter_by(category_id = category_id).all()
                bottles = list(map(lambda bottle: bottle.serialize(), bottles))
                return jsonify(bottles), 200
            #Condition for show all the bootles that are not in the route category_id
            elif boolean is 0:
                bottles = Bottle.query.filter(Bottle.category_id != category_id).all()
                bottles = list(map(lambda bottle: bottle.serialize(), bottles))
                return jsonify(bottles), 200
            else:
                return jsonify({"error":"Invalid Route"})
        else:
            bottles = Bottle.query.all()
            bottles = list(map(lambda bottle: bottle.serialize(), bottles))
            return jsonify(bottles), 200