import re
import uuid
import requests
from datetime import datetime
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reviewsapi.sqlite3"
app.config["TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()

# one to one relationship
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_uid = db.Column(db.String, nullable=False)    # this is a uuid4 entry
    door_num = db.Column(db.String(35), nullable=False)
    street = db.Column(db.String(60), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)
    geo_map = db.relationship('Maps', backref='location', uselist=False)
    reviews = db.relationship('Review', backref='address')
    buisnesses = db.relationship('Business', backref='place')
    incident = db.relationship('Incident', backref='area')

# one to many relationship
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_uid = db.Column(db.String, nullable=False)    # this is a uuid4 entry
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

# one to one relationship
class Maps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lon = db.Column(db.String(15), nullable=False)
    lat = db.Column(db.String(15), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

# one to many relationship
class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buisness_uid = db.Column(db.String, nullable=False)    # this is a uuid4 entry
    name = db.Column(db.String(60), nullable=False)
    category = db.Column(db.String(15), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

# one to many relationship with address
class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_uid = db.Column(db.String, nullable=False)    # this is a uuid4 entry
    category = db.Column(db.String(15), nullable=False) # this should be one word
    description = db.Column(db.String(40), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

# create all db models
db.create_all()

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
    find_id = db.session.query(Review).filter_by(id=review_id).first()
    if not find_id:
        abort(404, message="Could not find review")

def abort_if_review_exists(review_id):
    find_id = db.session.query(Review).filter_by(id=review_id).first()
    if find_id:
        abort(409, message="Review already exists with that ID...")

def abort_if_map_data_not_found(map_data):
    if map_data == []:
        abort(404, message="No coodinates found, please check your postcode.")

def abort_if_bad_request():
    abort(400, message="Oops, something went wrong with your request! Please check your details and try again...")

def abort_if_incorrect_rating(rating: int):
    if rating < 1 or rating > 5:
        abort(400, message="The rating must be between 1 and 5.")

def abort_if_incorrect_reviewee(reviewee):
    if reviewee not in ["tenant", "neighbour", "visitor"]:
        abort(400, message="Wrong reviewee type. Enter one of the following: 'tenant', 'neighbour' or 'visitor'")

def abort_if_not_uk_postcode(postcode):
    # Regular expression pattern for UK postcode validation with case-insensitive matching
    pattern = r"^(?i)[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z-[CIKMOV]]{2}$"
    # Remove any whitespace from the postcode
    postcode = postcode.replace(" ", "")
    # Check if the postcode matches the pattern
    if not re.match(pattern, postcode):
        abort(400, message="Please enter a valid UK postcode.")

def validate_door_request(door: str) -> bool:
    response = db.session.query(
        db.session.query(Address).filter_by(door_num=door).exists()
    ).scalar()
    return response

def validate_postcode_request(postcode: str) -> bool:
    response = db.session.query(
        db.session.query(Address).filter_by(postcode=postcode).exists()
    ).scalar()
    return response

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
        # query db to display json info
        return reviews[review_id]
    
    def put(self, review_id):
        abort_if_review_exists(review_id)
        args = community_review_put_args.parse_args()
        # get values from args.get("...")
        address_uuid = str(uuid.uuid4())
        review_uuid = str(uuid.uuid4())
        door = args.get("door").lower()
        street = args.get("street").lower()
        location = args.get("location").lower()
        postcode = args.get("postcode").lower()
        rating = args.get("rating")
        review = args.get("review")
        reviewee = args.get("reviewee").lower()
        abort_if_not_uk_postcode(postcode)
        abort_if_incorrect_reviewee(reviewee)
        # validate door requ1111est - check if one already exists
        validate_door = validate_door_request(door)
        # validate postcode - check if already exists
        validate_postcode = validate_postcode_request(postcode)
        # convert postcode to longitude & latitude
        OPENSTREETMAP_URL = "https://nominatim.openstreetmap.org/search?format=json"
        map_response = requests.get(f"{OPENSTREETMAP_URL}&postalcode={postcode}&country=united kingdom")
        map_data = map_response.json()
        # abort if no coordinates found with postcode
        abort_if_map_data_not_found(map_data)
        # if postcode is false, create an address entry
        if validate_postcode == False:
            # if coodinates exist create address, review & map entries
            if map_data:
                new_address_entry = Address(
                    address_uid=address_uuid,
                    door=door,
                    street=street,
                    location=location,
                    postcode=postcode
                )
                db.session.add(new_address_entry)
                db.session.commit()
                # update map db & review db if coodinates exists
                latitude = map_data[0].get("lat")
                longitude = map_data[0].get("lon")
                new_map_entry = Maps(
                    lon=longitude,
                    lat=latitude,
                    location=new_address_entry
                )
                db.session.add(new_map_entry)
                db.session.commit()
                new_review_entry = Review(
                    review_uid=review_uuid,
                    rating=rating,
                    review=review,
                    type=reviewee,
                    date=datetime.now(),
                    address=new_review_entry
                )
                db.session.add(new_review_entry)
                db.session.commit()
                # return data as json object.
                response = jsonify({
                    "id": new_review_entry.id,
                    "status": 201,
                    "Address": {
                        "id": new_address_entry.id,
                        "unique-address-id": new_address_entry.address_uid,
                        "Door": new_address_entry.door_num,
                        "Street": new_address_entry.street,
                        "Location": new_address_entry.location,
                        "Postcode": new_address_entry.postcode},
                    "Review": {
                        "id": new_review_entry.id,
                        "unique-review-id": new_review_entry.review_uid,
                        "Rating": new_review_entry.rating,
                        "Review": new_review_entry.review,
                        "Reviewee": new_review_entry.type,
                        "Timestamp": new_review_entry.date},
                    "Map": {
                        "id": new_map_entry.id,
                        "Longitude": new_map_entry.lon,
                        "Latitude": new_map_entry.lat},
                })
                response.header["Custom-Header"] = "New address, review & map coordinates created successfully."
                return response, 201
            else:
                abort_if_bad_request()  
        # if postcode matches but diff door number - create new address, review, map
        if (validate_door == False) and validate_postcode == True:
            # if coodinates exist create address, review & map entries
            if map_data:
                new_address_entry = Address(
                    address_uid=address_uuid,
                    door=door,
                    street=street,
                    location=location,
                    postcode=postcode
                )
                db.session.add(new_address_entry)
                db.session.commit()
                # update map db & review db if coodinates exists
                latitude = map_data[0].get("lat")
                longitude = map_data[0].get("lon")
                new_map_entry = Maps(
                    lon=longitude,
                    lat=latitude,
                    location=new_address_entry
                )
                db.session.add(new_map_entry)
                db.session.commit()
                new_review_entry = Review(
                    review_uid=review_uuid,
                    rating=rating,
                    review=review,
                    type=reviewee,
                    date=datetime.now(),
                    address=new_review_entry
                )
                db.session.add(new_review_entry)
                db.session.commit()
                # return data as json object.
                response = jsonify({
                    "id": new_review_entry.id,
                    "status": 201,
                    "Address": {
                        "id": new_address_entry.id,
                        "unique-address-id": new_address_entry.address_uid,
                        "Door": new_address_entry.door_num,
                        "Street": new_address_entry.street,
                        "Location": new_address_entry.location,
                        "Postcode": new_address_entry.postcode},
                    "Review": {
                        "id": new_review_entry.id,
                        "unique-review-id": new_review_entry.review_uid,
                        "Rating": new_review_entry.rating,
                        "Review": new_review_entry.review,
                        "Reviewee": new_review_entry.type,
                        "Timestamp": new_review_entry.date},
                    "Map": {
                        "id": new_map_entry.id,
                        "Longitude": new_map_entry.lon,
                        "Latitude": new_map_entry.lat},
                })
                response.header["Custom-Header"] = "New address, review & map coordinates created successfully."
                return response, 201
        # if door & postcode match - create review from existing address db (query db and link address id to new review foreign key)
        if (validate_door == True) and validate_postcode == True:
            # get db object of matching address
            find_address = db.session.query(Address).filter_by(door_num=door, postcode=postcode).first()
            # create a new review
            new_review_entry = Review(
                review_uid=review_uuid,
                rating=rating,
                review=review,
                type=reviewee,
                date=datetime.now(),
                address=new_review_entry
            )
            db.session.add(new_review_entry)
            db.session.commit()
            response = jsonify({
                "id": new_review_entry.id,
                "status": 201,
                "Address": {
                    "id": find_address.id,
                    "unique-address-id": find_address.address_uid,
                    "Door": find_address.door_num,
                    "Street": find_address.street,
                    "Location": find_address.location,
                    "Postcode": find_address.postcode},
                "Review": {
                    "id": new_review_entry.id,
                    "unique-review-id": new_review_entry.review_uid,
                    "Rating": new_review_entry.rating,
                    "Review": new_review_entry.review,
                    "Reviewee": new_review_entry.type,
                    "Timestamp": new_review_entry.date},
                "Map": {
                    "id": new_map_entry.id,
                    "Longitude": new_map_entry.lon,
                    "Latitude": new_map_entry.lat},
            })
            response.header["Custom-Header"] = "New review successfully created using existing address."
            return response, 201

    
    def delete(self, review_id):
        abort_if_review_id_not_found(review_id)
        del reviews[review_id]
        return '', 204
    

api.add_resource(HelloWorld, "/helloworld")
api.add_resource(CommunityReview, "/review/<int:review_id>")

if __name__ == "__main__":
    app.run(debug=True)