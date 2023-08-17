from datetime import datetime

from flask import Flask, abort, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import Campsite, Park, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Note: `app.json.compact = False` Configures JSON responses to print on indented lines
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Parks(Resource):
    ##INDEX
    def get(self):
        parks = [park.to_dict() for park in Park.query.all()]
        return make_response(parks, 200)

api.add_resource(Parks, "/parks")
    
class ParkById(Resource):
    ##SHOW
    def get_Park_by_id(self, id):
        park = park.query.filter_by(Park.id == id).first().to_dict()
        return make_response(park, 200)

api.add_resource(ParkById, "/parks/<int:id>")
   
class Campsites(Resource):
    ##INDEX
    def get(self):
        campsites = [campsite.to_dict() for campsite in Campsite.query.all()]
        return make_response(campsites, 200) 
    def post_campsite(self):
        data = request.get_json()
        new_campsite = Campsite(
            park_id=['park_id'],
            max_capacity=['max_capacity'],
            type=['type'],
            site_fee=['site_fee'],
            has_water=['has_water'],
            has_bathroom=['has_bathroom'],
            has_grill=['has_grill'],              
        )
        db.session.add(new_campsite)
        db.session.commit()
        return make_response(new_campsite.to_dict(), 201)

api.add_resource(Campsites, "/campsites")
        
class CampsiteById(Resource):
    ##SHOW
    def get_campsite_by_id(self, id):
        campsite = Campsite.query.filter_by(Campsite.id == id).first().to_dict()
        return make_response(campsite, 200)
    ##UPDATE
    def update_campsite(self, id):
        data = request.json()
        campsite = Campsite.query.get_or_404(id).to_dict()
        
        for key, value in data.items():
            setattr(self, key, value)
        db.session.add(campsite)
        db.session.commit()
        
        return make_response(campsite.to_dict(), 202)
    
    ##DESTROY
    def destroy_campsite(self, id):
        campsite = Campsite.query.get_or_404(id).to_dict() 
        db.session.delete(campsite)
        db.commit()

class Reservations():
    pass
    
api.add_resource(CampsiteById, "/campsites/<int:id>")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
