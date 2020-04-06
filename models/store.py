from db import db
from flask_sqlalchemy import SQLAlchemy

class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    location = db.Column(db.String(80))

    items = db.relationship('ItemModel')

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def get_json(self):
        return {
            'name': self.name,
            'location': self.location,
            'items': [item.get_json() for item in self.items]
            }

    @classmethod
    def find_store_by_name(cls, name):
        '''
        looks for an entry with name in DB
        retuns ItemModel type object
        '''
        return StoreModel.query.filter_by(name=name).first()

    def save_to_db(self):
        '''
        save item into DB
        '''
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        '''
        Update item {dict} into DB
        '''
        db.session.delete(self)
        db.session.commit()