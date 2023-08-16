from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import Project, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Note: `app.json.compact = False` Configures JSON responses to print on indented lines
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Projects(Resource):
    pass


if __name__ == "__main__":
    app.run(port=5000, debug=True)
