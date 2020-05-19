from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
db = SQLAlchemy()

class Consumer(db.Model):
    __tablename__ = 'consumers'
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String(255), nullable = True)
    
    def __repr__(self):
        return 'Consumer %r' % self.email

    def serialize(self):
        return{
            'id': self.id,
            'email': self.email
        }

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumers.id'), nullable = False)
    consumer = db.relationship(Consumer, backref = backref('children', cascade = 'all, delete'))
    
    def __repr__(self):
        return 'Category %r' % self.name

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'consumer': self.consumer.serialize()
        }

class Bottle(db.Model):
    __tablename__ = 'bottles'
    id = db.Column(db.Integer,primary_key = True)
    country = db.Column(db.String(255), nullable = False)
    image = db.Column(db.String(255), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)
    category = db.relationship(Category, backref = backref('children', cascade = 'all, delete'))
    
    def __repr__(self):
        return 'Bottle %r' % self.country

    def serialize(self):
        return{
            'id': self.id,
            'country': self.country,
            'image': self.image,
            'category': self.category.serialize()
        }

