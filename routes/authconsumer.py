from flask import Flask, render_template, jsonify, request, Blueprint
from flask_jwt_extended import (
    create_access_token, get_jwt_identity
)
from flask_bcrypt import Bcrypt
from models import db, Consumer

bcrypt = Bcrypt()
authconsumer = Blueprint('authconsumer', __name__)
@authconsumer.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    if not email:
        return jsonify({"error": "You need insert your email"}), 422
    if not password:
        return jsonify({"error": "You need insert your password"}), 422
    consumer = Consumer.query.filter_by(email=email).first()
    if not consumer:
        return jsonify({"error": "Email is not correct"}), 404
    pw_hash = bcrypt.generate_password_hash(password)
    if bcrypt.check_password_hash(consumer.password, password):
        access_token = create_access_token(identity=consumer.email)
        data = {
            "access_token": access_token,
            "consumer": consumer.serialize()
        }
        return jsonify(data), 200
    else: 
        return jsonify({"error": "Email or password is not correct"}), 401
        
@authconsumer.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    if not email:
        return jsonify({"error": "You need to write yor email"}), 422
    if not password:
        return jsonify({"error": "You need to write your password"}), 422 
    consumer = Consumer.query.filter_by(email=email).first()
    if consumer:
        return jsonify({"error": "This email already exist"}), 422
    consumer = Consumer()
    consumer.email = email
    consumer.password = bcrypt.generate_password_hash(password)
    db.session.add(consumer)
    db.session.commit()
    if bcrypt.check_password_hash(consumer.password, password):
        access_token = create_access_token(identity=consumer.email)
        data = {
            "access_token": access_token,
            "consumer": consumer.serialize()
        }
        return jsonify(data), 200
    else: 
        return jsonify({"error": "Email or password are incorrect"}), 401


