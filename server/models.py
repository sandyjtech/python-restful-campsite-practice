from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Park(db.Model, SerializerMixin):
    __tablename__ = "parks"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String, nullable=False)
    entrance_fee = db.Column(db.Float, nullable=False)
    has_trails = db.Column(db.Boolean)
    has_RV_cleanout = db.Column(db.Boolean)
    begin_camping_season = db.Column(db.DateTime)
    end_camping_season = db.Column(db.DateTime)
    
    @validates("entrance_fee")
    def validate_entrance_fee(self, key, value):
        if not 13.99 <= value <= 25.00:
            raise ValueError("Entrance fee must be between 13.99 and 25.00")
        return value  # Don't forget to return the validated value
    
    campsites = db.relationship("Campsite", backref="park")
        
    def __repr__(self):
        return f'<Park name: {self.name}, address: {self.address}>'

class Campsite(db.Model, SerializerMixin):
    __tablename__ = "campsites"
    
    id = db.Column(db.Integer, primary_key=True)
    park_id = db.Column(db.Integer, db.ForeignKey('parks.id'))
    max_capacity = db.Column(db.Integer)
    type = db.Column(db.String)
    site_fee = db.Column(db.Float)
    has_water = db.Column(db.Boolean)
    has_bathroom = db.Column(db.Boolean)
    has_grill = db.Column(db.Boolean)
    
    @validates("max_capacity")
    def validate_max_capacity(self, key, value):
        if not value <= 10:
            raise ValueError("Max capacity must be 10 or less")
        return value  # Don't forget to return the validated value
    
    @validates("type")
    def validate_type(self, key, value):
        if value not in ['tent', 'RV']:
            raise ValueError("Type must be tent or RV")
        return value  # Don't forget to return the validated value
    
    reservation = db.relationship("Reservation", backref="campsite")
    
    def __repr__(self):
        return f'<Campsite id:{self.id}, type: {self.type}, site fee: {self.site_fee}>'

class Reservation(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    campsite_id = db.Column(db.Integer, db.ForeignKey('campsites.id'))  # Add this line
    
    @validates('start_date')
    def validate_start_date(self, key, start_date):
        if not (self.campsite.park.begin_camping_season <= start_date <= self.campsite.park.end_camping_season):
            raise ValueError("Reservation start date must be between start season and end season dates")
        return start_date
    
    @validates('end_date')
    def validate_end_date(self, key, end_date):
        if not (self.campsite.park.begin_camping_season <= end_date <= self.campsite.park.end_camping_season):
            raise ValueError("Reservation end date must be between start season and end season dates")
        return end_date