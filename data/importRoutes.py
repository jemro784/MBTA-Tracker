import json
import psycopg2

with open('routes.json', 'r') as f:
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
    geometry = json.dumps(feature['geometry'])
    
    query = f"INSERT INTO Routes (route, line, geometry) VALUES ('{properties['ROUTE']}', '{properties['LINE']}', ST_SetSRID(ST_GeomFromGeoJSON('{geometry}'), 4326))"
    
    cur.execute(query)

conn.commit()
cur.close()
conn.close()