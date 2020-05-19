from flask import Flask, render_template, jsonify, request, Blueprint
from models import db, Bottle
from flask_jwt_extended import (
    jwt_required
)

route_bootles = Blueprint('route_bootles', __name__)
@route_bootles.route('/bootles', methods=['GET','POST'])
@route_bootles.route('/bootles/<int:id>', methods=['GET','DELETE'])
@route_bootles.route('/bootles/category/<int:category_id>/<int:boolean>', methods=['GET'])
@jwt_required
def bottles(id=None, category_id=None, boolean=1):
    if request.method == 'GET':
        if id is not None:
            bottle = Bottle.query.get(id)
            if bottle:
                return jsonify(bottle.serialize()), 200
            else:
                return jsonify({"msg":"Not Found"}), 404
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
                return jsonify({"msg":"Invalid Route"})
        else:
            bottles = Bottle.query.all()
            bottles = list(map(lambda bottle: bottle.serialize(), bottles))
            return jsonify(bottles), 200

    if request.method == 'POST':
        country = request.json.get('country')
        image = request.json.get('image')
        category_id = request.json.get('category_id')
        if not country:
            return jsonify({"msg":"Country is required"}), 422
        if not image:
            return jsonify({"msg":"Image is required"}), 422
        if not category_id:
            return jsonify({"msg":"Category is required"}), 422
        bottle = Bottle()
        bottle.country = country
        bottle.image = image
        bottle.category_id = category_id
        db.session.add(bottle)
        db.session.commit()
        return jsonify(bottle.serialize()), 201

    if request.method == 'DELETE':
        bottle = Bottle.query.get(id)
        db.session.delete(bottle)
        db.session.commit()
        return jsonify({"msg":"Deleted"}), 200