from flask import Blueprint, jsonify, request
from models import db, Bottle

bootles = Blueprint('bootles', __name__)
@bootles.route('/bootles', methods=['GET','POST'])
@bootles.route('/bootles/<int:id>', methods=['GET','DELETE'])
@bootles.route('/bootles/category/<int:category_id>', methods=['GET'])
@bootles.route('/bootles/category/<int:category_id>/bootle/<int:id>', methods=['GET'])
@jwt_required
def bottles(id=None, category_id=None):
    if request.method == 'GET':
        if id is not None and category_id is not None:
            bottle = Bottle.query.filter_by(category_id = category_id, id = id).first()
            if bottle:
                return jsonify(bottle.serialize()), 200
            else:
                return jsonify({"msg":"Not Found"}), 404
        elif id is not None:
            bottle = Bottle.query.get(id)
            if bottle:
                return jsonify(bottle.serialize()), 200
            else:
                return jsonify({"msg":"Not Found"}), 404
        elif category_id is not None:
            bottles = Bottle.query.filter_by(category_id = category_id).first()
            bottles = list(map(lambda bottle: bottle.serialize(), bottles))
            return jsonify(bottles), 200
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