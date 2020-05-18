from flask import Blueprint, jsonify, request
from models import db, Exchange

bootles = Blueprint('bootles', __name__)
@route_exchanges.route('/exchanges', methods=['GET','POST'])
@route_exchanges.route('/exchanges/<int:id>', methods=['GET', 'DELETE'])
@route_exchanges.route('/exchanges/consumer/<int:consumer_id>', methods=['GET', 'POST'])
@route_exchanges.route('/exchanges/consumer/<int:consumer_id>/exchange/<int:id>', methods=['GET', 'POST'])
@jwt_required
def exchange(id=None, consumer_id = None):
    if request.method == 'GET':
        if id is not None and consumer_id is not None:
            exchange = Exchage.query.filter_by(consumer_id = consumer_id, id = id).first()
            if exchange:
                return jsonify(exchange.serialize()), 200
            else:
                return jsonify({"exchange":"Not found"}), 404
        elif id is not None:
            exchange = Exchage.query.get(id)
            if exchange:
                return jsonify(exchange.serialize()), 200
            else:
                return jsonify({"exchange": "Not found"})
        elif consumer_id is not None:
            exchanges = Exchage.query.filter_by(consumer_id=consumer_id).all()
            exchanges = list(map(lambda exchange: exchange.serialize(),exchanges))
            return jsonify(exchanges), 200
        else:
            exchanges = Exchage.query.all()
            exchanges = list(map(lambda exchange: exchange.serialize(),exchanges))
            return jsonify(exchanges), 200

    if request.method == 'POST':
        image = request.json.get('image')
        country = request.json.get('country')
        consumer_id = request.json.get('consumer_id')
        if not image:
            return jsonify({"msg": "image is required"}), 422 
        if not country:
            return jsonify({"msg": "country is required"}), 422 
        if not consumer_id:
            return jsonify({"msg": "consumer_id is required"}), 422 

        exchange = Exchage()
        exchange.image = image
        exchange.country = country
        exchange.consumer_id = consumer_id
        db.session.add(exchange)
        db.session.commit()
        return jsonify(exchange.serialize()), 201
    
 
    if request.method == 'DELETE':
        
        exchange = Exchage.query.get(id)
        db.session.delete(exchange)
        db.session.commit()
        return jsonify({'exchange':'Deleted'}), 200