import React, { useEffect, useState, useRef } from 'react';
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import '../../App.css';

const LeafletComponent = () => {
  const mapContainerRef = useRef(null);
  const map = useRef(null);

  const [lng] = useState(24.926);
  const [lat] = useState(60.227);
  const [zoom] = useState(12);

  const [markers, setMarkers] = useState([]);

  useEffect(() => {
    map.current = L.map(mapContainerRef.current).setView([lat, lng], zoom);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors",
    }).addTo(map.current);

    map.current.on('click', (e) => {
      const { lat, lng } = e.latlng;
      const newMarker = { id: Date.now(), lat, lng, description: "" };
      setMarkers((prevMarkers) => [...prevMarkers, newMarker]);
    });

    return () => {
      map.current.remove();
    };
  }, [lat, lng, zoom]);

  useEffect(() => {
    markers.forEach(marker => {
      const customIcon = L.icon({
        iconUrl: 'https://leafletjs.com/examples/custom-icons/leaf-red.png',
        iconSize: [38, 95],
        iconAnchor: [22, 94],
        popupAnchor: [-3, -76],
      });

      const markerInstance = L.marker([marker.lat, marker.lng], { icon: customIcon }).addTo(map.current);

      const popupContent = document.createElement('div');
      popupContent.innerHTML = `
        <b>Marker at</b><br>Lat: ${marker.lat}<br>Lng: ${marker.lng}<br>
        <input type="text" id="desc-${marker.id}" class="marker-input" placeholder="Enter description" value="${marker.description}" />
        <button id="delete-${marker.id}" class="marker-delete-btn">Delete</button>
      `;

      markerInstance.bindPopup(popupContent);

      markerInstance.on('popupopen', () => {
        const buttonElement = popupContent.querySelector(`#delete-${marker.id}`);

        const deleteMarker = (e) => {
          e.preventDefault();
          e.stopPropagation();
          setMarkers((prevMarkers) => prevMarkers.filter(m => m.id !== marker.id));
          map.current.removeLayer(markerInstance);
        };
        buttonElement.addEventListener('click', deleteMarker);
      });
    });
  }, [markers]);

  return (
    <div>
      <div className="map-container" ref={mapContainerRef} style={{ height: '80vh', width: '100%' }} />
    </div>
  );
};

export default LeafletComponent;
