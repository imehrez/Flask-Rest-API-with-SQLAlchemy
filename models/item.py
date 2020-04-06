from db import db

class ItemModel(db.Model):
    # db.model things that are to be stored (related) in database
    
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def get_json(self):
        return {'name':self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        '''
        looks for an entry with name in DB
        retuns ItemModel type object
        '''
        return ItemModel.query.filter_by(name=name).first()

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