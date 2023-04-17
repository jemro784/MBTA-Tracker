import requests
import psycopg2

conn = psycopg2.connect(
    host='',
    database='',
    user='',
    password=''
)

url = 'https://api-v3.mbta.com/stops?filter[route_type]=0,1'


response = requests.get(url)

data = response.json()

cur = conn.cursor()

for station in data['data']:
    id = station['id']
    name = station['attributes']['name']

    cur.execute(
        'INSERT INTO Stations (id, name) VALUES (%s, %s)',
        (id, name)
    )

conn.commit()
cur.close()
conn.close()