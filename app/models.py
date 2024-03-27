from . import db
import enum
from sqlalchemy import Integer, Enum

class PropertyType(enum.Enum):
    house = 'house'
    apartment = 'apartment'

class PropertyProfile(db.Model):
    __tablename__ = 'property_profiles'

    id = db.Column(db.Integer, primary_key=True)
    prop_title = db.Column(db.String(120))
    prop_description = db.Column(db.String(1000))
    prop_rooms = db.Column(db.Integer)
    prop_bathrooms = db.Column(db.Integer)
    prop_price = db.Column(db.Numeric(10, 0))
    prop_type = db.Column(db.Enum(PropertyType))
    prop_location = db.Column(db.String(120))


    def __init__(self, prop_title, prop_description, prop_rooms, prop_bathrooms,
                 prop_price, prop_type, prop_location):

        super().__init__()
        
        self.prop_title = prop_title
        self.prop_description = prop_description
        self.prop_rooms =  prop_rooms
        self.prop_bathrooms =  prop_bathrooms
        self.prop_price = prop_price
        self.prop_type = prop_type
        self.prop_location = prop_location
        

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support



