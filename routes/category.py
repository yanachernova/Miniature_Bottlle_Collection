from flask import Blueprint, request, jsonify
from models import db, Category
from flask_jwt_extended import (
    jwt_required
)
route_categories = Blueprint('route_categories', __name__)
@route_categories.route('/categories', methods=['GET','POST'])
@route_categories.route('/categories/<int:id>', methods=['GET', 'DELETE'])
@route_categories.route('/categories/consumer/<int:consumer_id>', methods=['GET', 'POST'])
@route_categories.route('/categories/consumer/<int:consumer_id>/category/<int:id>', methods=['GET', 'POST'])
@jwt_required
def categories(id=None, consumer_id = None):
    if request.method == 'GET':
        if id is not None and consumer_id is not None:
            category = Category.query.filter_by(consumer_id = consumer_id, id = id).first()
            if category:
                return jsonify(category.serialize()), 200
            else:
                return jsonify({"category":"Not found"}), 404
        elif id is not None:
            category = Category.query.get(id)
            if category:
                return jsonify(category.serialize()), 200
            else:
                return jsonify({"category": "Not found"})
        elif consumer_id is not None:
            categories = Category.query.filter_by(consumer_id=consumer_id).all()
            categories = list(map(lambda category: category.serialize(),categories))
            return jsonify(categories), 200
        else:
            categories = Category.query.all()
            categories = list(map(lambda category: category.serialize(),categories))
            return jsonify(categories), 200

    if request.method == 'POST':
        name = request.json.get('name')
        consumer_id = request.json.get('consumer_id')
        if not name:
            return jsonify({"msg": "Name is required"}), 422 
        if not consumer_id:
            return jsonify({"msg": "consumer_id is required"}), 422 

        category = Category()
        category.name = name
        category.consumer_id = consumer_id
        db.session.add(category)
        db.session.commit()
        return jsonify(category.serialize()), 201
    
    if request.method == 'PUT':
        
        category = Category.query.get(id)
        category.name = request.json.get('name')
        db.session.commit()
        return jsonify(category.serialize()), 200

    if request.method == 'DELETE':
        
        category = Category.query.get(id)
        db.session.delete(category)
        db.session.commit()
        return jsonify({'category':'Deleted'}), 200