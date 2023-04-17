from flask import Flask, jsonify
import json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_AsGeoJSON

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
db = SQLAlchemy(app)

app.app_context().push()

class Stops(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    station = db.Column(db.String(100))
    line = db.Column(db.String(100))
    route = db.Column(db.String(100))
    geometry = db.Column(Geometry(geometry_type = 'POINT', srid=4326))

    def __init__(self, station, line, route, geometry):
        self.station = station
        self.line = line
        self.route = route
        self.geometry = geometry

class Routes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    route = db.Column(db.String(100))
    line = db.Column(db.String(100))
    geometry = db.Column(Geometry(geometry_type = 'MULTILINESTRING', srid=4326))

    def __init__(self, route, line, geometry):
        self.route = route
        self.line = line
        self.geometry = geometry

class Vehicles(db.Model):
    id = db.Column(db.String(100), primary_key = True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    status = db.Column(db.String(100))
    bearing = db.Column(db.Integer)
    route = db.Column(db.String(100))
    stop_id = db.Column(db.String(100), db.ForeignKey('stations.id'))
    stop = db.relationship('Stations', backref=db.backref('vehicles', lazy=True))
    predictions = db.relationship('Predictions', backref=db.backref('vehicle', lazy=True))

    def __init__(self, id, latitude, longitude, status, bearing, route, stop_id):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.status = status
        self.bearing = bearing
        self.route = route
        self.stop_id = stop_id

class Stations(db.Model):
    id = db.Column(db.String(100), primary_key = True)
    name = db.Column(db.String(100))

    def __init__(self, id, name):
        self.id = id
        self.name = name

class Predictions(db.Model):
    id = db.Column(db.String(100), primary_key = True)
    arrival = db.Column(db.String(100))
    departure = db.Column(db.String(100))
    vehicle_id = db.Column(db.String(100), db.ForeignKey('vehicles.id'))

    def __init__(self, id, arrival, departure, vehicle_id):
        self.id = id
        self.arrival = arrival
        self.departure = departure
        self.vehicle_id = vehicle_id

@app.route('/stops', methods = ['GET'])
def get_stops():
    stops = Stops.query.all()
    data = {'type': 'FeatureCollection', 'features': []}
    for stop in stops:
        feature = {
            'type': 'Feature',
            'geometry': json.loads(db.session.scalar(ST_AsGeoJSON(stop.geometry))),
            'properties': {
                'id': stop.id,
                'station': stop.station,
                'line': stop.line,
                'route': stop.route
            }
        }
        data['features'].append(feature)
    return jsonify(data)

@app.route('/routes', methods = ['GET'])
def get_routes():
    routes = Routes.query.all()
    data = {'type': 'FeatureCollection', 'features': []}
    for route in routes:
        feature = {
            'type': 'Feature',
            'geometry': json.loads(db.session.scalar(ST_AsGeoJSON(route.geometry))),
            'properties': {
                'id': route.id,
                'route': route.route,
                'line': route.line
            }
        }
        data['features'].append(feature)
    return jsonify(data)

@app.route('/vehicles', methods = ['GET'])
def get_vehicles():
    vehicles = Vehicles.query.all()
    data = {'attributes': []}
    for vehicle in vehicles:
        stop_name = vehicle.stop.name if vehicle.stop is not None else None
        predictions = vehicle.predictions
        arrival = None
        departure = None
        if predictions:
            arrival = predictions[0].arrival
            departure = predictions[0].departure
        attribute = {
            'id': vehicle.id,
            'latitude': vehicle.latitude,
            'longitude': vehicle.longitude,
            'status': vehicle.status,
            'bearing': vehicle.bearing,
            'route': vehicle.route,
            'stop': stop_name,
            'arrival': arrival,
            'departure': departure
        }
        data['attributes'].append(attribute)
    return jsonify(data)

if __name__ == '__main__':
    app.run()