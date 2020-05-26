from flask import Blueprint, request, jsonify, current_app
from libs.functions import sendMail
from flask_jwt_extended import (
    jwt_required
)
route_email = Blueprint('route_email', __name__)
@route_email.route('/sendemail', methods=['POST'])
def sendemail():
    subject = '..::WEBSITE MESSAGE::..'
    to_email = current_app.config['MAIL_USERNAME']
    name = request.json.get('name', None)
    from_email = request.json.get('from_email', None)
    phone = request.json.get('phone', None)  
    message = request.json.get('message', None)

    if not name:
        return jsonify({"error": "Name is required"}), 422
    if not from_email:
        return jsonify({"error": "Email is required"}), 422
    if not phone:
        return jsonify({"error": "Phone is required"}), 422
    if not message:
        return jsonify({"error": "Message is required"}), 422

    sendMail(subject, 'Yana', to_email, to_email, '<div><p>This is a message from your web, check the information below:</p><p>Contact name: '+name+'</p><p>Contact phone: '+phone+'</p><p>Contact email: '+from_email+'</p><p>Contact message: '+message+'</p></div>')
    return jsonify({"success": "Email send successfully"}), 200
