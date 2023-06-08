import uuid
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reviewsapi.sqlite3"
# app.config["TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy()

# # one to one relationship
# class Address(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     address_uid = db.Column(db.String, nullable=False)    # this is a uuid4 entry
#     door_num = db.Column(db.String(35), nullable=False)
#     street = db.Column(db.String(60), nullable=False)
#     location = db.Column(db.String(50), nullable=False)
#     postcode = db.Column(db.String(10), nullable=False)
#     geo_map = db.relationship('Maps', backref='location', uselist=False)
#     reviews = db.relationship('Review', backref='address')
#     buisnesses = db.relationship('Business', backref='place')
#     incident = db.relationship('Incident', backref='area')

# # one to many relationship
# class Review(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     review_uid = db.Column(db.String, nullable=False)    # this is a uuid4 entry
#     rating = db.Column(db.Integer, nullable=False)
#     review = db.Column(db.Text, nullable=False)
#     type = db.Column(db.String(20), nullable=False)
#     date = db.Column(db.DateTime, nullable=False)
#     address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

# # one to one relationship
# class Maps(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     lon = db.Column(db.String(15), nullable=False)
#     lat = db.Column(db.String(15), nullable=False)
#     address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

# # one to many relationship
# class Business(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     buisness_uid = db.Column(db.String, nullable=False)    # this is a uuid4 entry
#     name = db.Column(db.String(60), nullable=False)
#     category = db.Column(db.String(15), nullable=False)
#     contact = db.Column(db.String(50), nullable=False)
#     address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

# # one to many relationship with address
# class Incident(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     incident_uid = db.Column(db.String, nullable=False)    # this is a uuid4 entry
#     category = db.Column(db.String(15), nullable=False) # this should be one word
#     description = db.Column(db.String(40), nullable=False)
#     date = db.Column(db.DateTime, nullable=False)
#     address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

# validate api arguments - reviews
community_review_put_args = reqparse.RequestParser()
community_review_put_args.add_argument("door", type=str, help="A door number is required...", required=True)
community_review_put_args.add_argument("street", type=str, help="A street name is required...", required=True)
community_review_put_args.add_argument("location", type=str, help="Place a town or city here...")
community_review_put_args.add_argument("postcode", type=str, help="A postocde is required...", required=True)
community_review_put_args.add_argument("rating", type=int, help="Please enter a value from 1 - 5", required=True)
community_review_put_args.add_argument("review", type=str, help="Place your review here...")
community_review_put_args.add_argument("reviewee", type=str, help="Enter one of the following: 'tenant', 'neighbour' or 'visitor'", required=True)
# validate api arguments - buisnesses
# validate api arguments - incidents

reviews = {}

def abort_if_review_id_not_found(review_id):
    if review_id not in reviews:
        abort(404, message="Could not find review")

def abort_if_review_exists(review_id):
    if review_id in reviews:
        abort(409, message="Review already exists with that ID...")

# api resources 
class HelloWorld(Resource):
    def get(self):
        response = jsonify({"note": "Hello World"})

        # create headers
        response.headers['Custom-Header'] = "Hello World resource"

        return response
    
class CommunityReview(Resource):
    def get(self, review_id):
        abort_if_review_id_not_found(review_id)
        return reviews[review_id]
    
    def put(self, review_id):
        abort_if_review_exists(review_id)
        args = community_review_put_args.parse_args()
        reviews[review_id] = {
            "id": review_id,
            "status": 201,
            "Address": {
                "unique-address-id": str(uuid.uuid4()),
                "Door": args.get("door"),
                "Street": args.get("street"),
                "Location": args.get("location"),
                "Postcode": args.get("poscode")},
            "Review": {
                "unique-review-id": str(uuid.uuid4()),
                "Rating": args.get("rating"),
                "Review": args.get("review"),
                "Reviewee": args.get("reviewee")},
            "Map": {
                "Longitude": 231548,
                "Latitude": 321549},
        }
        return reviews[review_id], 201
    
    def delete(self, review_id):
        abort_if_review_id_not_found(review_id)
        del reviews[review_id]
        return '', 204
    

api.add_resource(HelloWorld, "/helloworld")
api.add_resource(CommunityReview, "/review/<int:review_id>")

if __name__ == "__main__":
    app.run(debug=True)