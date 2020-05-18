from flask import jsonify
from flask_mail import Mail, Message
mail = Mail()

""" def sendMail(subject, name, from_email, to_email, msge): 
    msg = Message(subject, sender=[name, from_email], recipients=[to_email])
    msg.html = msge
    mail.send(msg)

    return jsonify({"msg":"Email send successfully"}),200 """

def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS