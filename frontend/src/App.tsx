import { useState, useEffect } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, Polyline, Marker, Popup} from 'react-leaflet';
import * as L from 'leaflet';
import './App.css';
import "leaflet-rotatedmarker"

function App() {
  const [vehicles, setVehicles] = useState([]);
  const [stops, setStops] = useState([]);
  const [routes, setRoutes] = useState([]);

  useEffect(() => {
    const fetchVehicles = async () => {
      const response = await axios.get('http://localhost:5000/vehicles');
      setVehicles(response.data.attributes);
    };

    const intervalId = setInterval(() => {
      const currentDate = new Date();
      const currentSeconds = currentDate.getSeconds();
      if (currentSeconds === 0 || currentSeconds === 30) {
        fetchVehicles();
      }
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);

  useEffect(() => {
    const fetchStops = async () => {
      const response = await axios.get('http://localhost:5000/stops');
      setStops(response.data.features);
    };
    const fetchRoutes = async () => {
      const response = await axios.get('http://localhost:5000/routes');
      setRoutes(response.data.features);
    };
    fetchStops();
    fetchRoutes();
  }, []);

  const redIcon = new L.Icon({
    iconUrl: require('./images/RedTrain.png'),
    iconSize: [28, 28],
    iconAnchor: [15, 15],
  });

  const orangeIcon = new L.Icon({
    iconUrl: require('./images/OrangeTrain.png'),
    iconSize: [28, 28],
    iconAnchor: [15, 15],
  });

  const greenIcon = new L.Icon({
    iconUrl: require('./images/GreenTrain.png'),
    iconSize: [28, 28],
    iconAnchor: [15, 15],
  });

  const blueIcon = new L.Icon({
    iconUrl: require('./images/BlueTrain.png'),
    iconSize: [28, 28],
    iconAnchor: [15, 15],
  });

  const stopIcon = new L.Icon({
    iconUrl: require('./images/MBTA.png'),
    iconSize: [18, 18],
    popupAnchor: [0, 0],
  });

  const iconMap = {
    'Red': redIcon,
    'Orange': orangeIcon,
    'Green-B': greenIcon,
    'Green-C': greenIcon,
    'Green-D': greenIcon,
    'Green-E': greenIcon,
    'Blue': blueIcon,
  };

  return (
    <MapContainer center={[42.331883, -71.052964]} zoom={11} scrollWheelZoom={true}>
      <TileLayer
        attribution="© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>"
        url=""
      />

      {routes.map(feature => (
        <Polyline
          key={feature.properties.id}
          positions={feature.geometry.coordinates.map(coords => coords)}
          color={feature.properties.line.toLowerCase()}
        />
      ))}

      {vehicles.map(vehicle => {
        return (
          <Marker 
            key={vehicle.id} 
            position={[vehicle.latitude, vehicle.longitude]}
            icon={iconMap[vehicle.route]}
            rotationAngle={vehicle.bearing}>
            <Popup
              position={[vehicle.latitude, vehicle.longitude]}>
              <div>
                <h2>{vehicle.id}</h2>
                <p>{"Current Status: " + vehicle.status + " " + vehicle.stop}</p>
                <p>{"Arrival Time: " + vehicle.arrival}</p>
                <p>{"Departure Time: " + vehicle.departure}</p>
              </div>
            </Popup>
          </Marker>
        );
      })}

      {stops.map(stop => (
        <Marker 
          key = {stop.properties.id} 
          position={[stop.geometry.coordinates[1], stop.geometry.coordinates[0]]} 
          icon={stopIcon}>
          <Popup 
            position={[stop.geometry.coordinates[1], stop.geometry.coordinates[0]]}>
            <div>
              <h2>{stop.properties.station}</h2>
              <p>{"Line: " + stop.properties.line}</p>
              <p>{"Route: " + stop.properties.route}</p>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default App;