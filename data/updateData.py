import requests
import psycopg2
from datetime import datetime

api_key = ''

conn = psycopg2.connect(
    host='',
    database='',
    user='',
    password=''
)

cur = conn.cursor()
cur.execute("DELETE FROM Predictions")
cur.execute("DELETE FROM Vehicles")

urlVehicles = f'https://api-v3.mbta.com/vehicles?filter[route]=Red,Blue,Green-B,Green-C,Green-D,Green-E,Orange&api_key={api_key}'
urlPredictions = f'https://api-v3.mbta.com/predictions?filter[route]=Red,Blue,Green-B,Green-C,Green-D,Green-E,Orange&api_key={api_key}'


responseVehicles = requests.get(urlVehicles)
responsePredictions = requests.get(urlPredictions)

dataVehicles = responseVehicles.json()
dataPredictions = responsePredictions.json()

for vehicle in dataVehicles['data']:
    id = vehicle['id']
    latitude = vehicle['attributes']['latitude']
    longitude = vehicle['attributes']['longitude']
    status = vehicle['attributes']['current_status']
    bearing = vehicle['attributes']['bearing']
    route = vehicle['relationships']['route']['data']['id']
    stop_id = None
    if vehicle['relationships']['stop']['data'] is not None:
        stop_id = vehicle['relationships']['stop']['data']['id']

    cur.execute(
        'INSERT INTO Vehicles (id, latitude, longitude, status, bearing, route, stop_id) VALUES (%s, %s, %s, %s, %s, %s, %s)',
        (id, latitude, longitude, status, bearing, route, stop_id)
    )

for prediction in dataPredictions['data']:
    id = prediction['id']
    if prediction['attributes']['arrival_time'] is not None:
        arrival = datetime.fromisoformat(str(prediction['attributes']['arrival_time']))
        arrivalTime = arrival.time()
        arrivalStr = arrivalTime.strftime("%I:%M %p")
    else:
        arrivalStr = 'N/A'
    if prediction['attributes']['departure_time'] is not None:
        departure = datetime.fromisoformat(str(prediction['attributes']['departure_time']))
        departureTime = departure.time()
        departureStr = departureTime.strftime("%I:%M %p")
    else:
        departureStr = 'N/A'
    vehicle_id = prediction['relationships']['vehicle']['data']['id']

    cur.execute(
        'INSERT INTO Predictions (id, arrival, departure, vehicle_id) VALUES (%s, %s, %s, %s)',
        (id, arrivalStr, departureStr, vehicle_id)
    )

conn.commit()
cur.close()
conn.close()