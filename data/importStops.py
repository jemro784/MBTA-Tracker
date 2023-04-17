import json
import psycopg2

with open('stops.json', 'r') as f:
    data = json.load(f)

conn = psycopg2.connect(
    host='',
    database='',
    user='',
    password=''
)

cur = conn.cursor()

for feature in data['features']:
    properties = feature['properties']
    geometry = feature['geometry']
    coordinates = geometry['coordinates']
    point = f'POINT({coordinates[1]} {coordinates[0]})'

    cur.execute(
        'INSERT INTO Stops (station, line, route, geometry) VALUES (%s, %s, %s, ST_GeomFromText(%s, 4326))',
        (properties['STATION'], properties['LINE'], properties['ROUTE'], point)
    )

conn.commit()
cur.close()
conn.close()