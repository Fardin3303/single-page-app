import React, { useEffect, useState, useRef } from 'react';
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import '../../App.css';
import { getPoints, createPoint, updatePoint, deletePoint } from '../../api/api';

const LeafletComponent = () => {
  const mapContainerRef = useRef(null);
  const map = useRef(null);

  const [lng] = useState(24.926);
  const [lat] = useState(60.227);
  const [zoom] = useState(12);

  const [markers, setMarkers] = useState([]);

  // Function to update marker description in state
  const updateMarkerDescription = (markerId, newDescription) => {
    setMarkers((prevMarkers) =>
      prevMarkers.map((marker) =>
        marker.id === markerId ? { ...marker, description: newDescription } : marker
      )
    );
  };

  useEffect(() => {
    map.current = L.map(mapContainerRef.current).setView([lat, lng], zoom);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors",
    }).addTo(map.current);

    map.current.on('click', (e) => {
      const { lat, lng } = e.latlng;
      // Ask user to insert description for the point
      const description = prompt("Please enter the description for the point", "Description");
      if (!description) {
        // Ask user to insert description for the point
        alert("Description is required");
        return;
      }
      const pointData = { description: description, latitude: lat.toString(), longitude: lat.toString(), created_at: new Date().toISOString() };
      const token = 'your_token_here';
      // console.log("Lat, Lon : " + lat + ", " + lng);
      // console.log("type of lat, lon : " + typeof(lat) + ", " + typeof(lng));
      // console.log("pointData : " + pointData);
      // console.log(getPoints)
      createPoint(pointData, token)
      .then((data) => {
        console.log('Point created successfully:', data);
      })
      .catch((error) => {
        console.error('Error creating point:', error);
      }
      );
      const newMarker = { id: Date.now(), lat, lng, description };
      setMarkers((prevMarkers) => [...prevMarkers, newMarker]);
    });

    return () => {
      map.current.remove();
    };
  }, [lat, lng, zoom]);

  useEffect(() => {
    markers.forEach((marker) => {
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
        <button id="update-${marker.id}" class="marker-update-btn">Update</button>
        <button id="delete-${marker.id}" class="marker-delete-btn">Delete</button>
      `;

      markerInstance.bindPopup(popupContent);

      markerInstance.on('popupopen', () => {
        const updateButton = popupContent.querySelector(`#update-${marker.id}`);
        const deleteButton = popupContent.querySelector(`#delete-${marker.id}`);
        const descriptionInput = popupContent.querySelector(`#desc-${marker.id}`);

        // Update marker description event
        updateButton.addEventListener('click', () => {
          const newDescription = descriptionInput.value;

          // Update the marker description in state
          updateMarkerDescription(marker.id, newDescription);

          // Call the API to update the marker description on the server
          const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzYWVpZCIsImV4cCI6MTcxODM1NTc4OX0.mxq_fmrCaHsda_iV2r2X0bTcjDPpsSq3zFBforEsOyg'; // Replace with your actual token
          updatePoint(marker.id, newDescription, token)
            .then((updatedPoint) => {
              console.log('Point updated successfully:', updatedPoint);
              // Optionally update state with the response if needed
            })
            .catch((error) => {
              console.error('Error updating point:', error);
              // Handle error state or display error message
            });

          markerInstance.closePopup();
        });

        // Delete marker event
        deleteButton.addEventListener('click', () => {
          setMarkers((prevMarkers) => prevMarkers.filter((m) => m.id !== marker.id));
          console.log("Asking to delete marker with id: " + marker.id);
          const token = 'your token here';
          // Call the API to delete the marker on the server
          deletePoint(marker.id, token)
            .then((deletedPoint) => {
              console.log('Point deleted successfully:', deletedPoint);
              // Optionally update state with the response if needed
            })
            .catch((error) => {
              console.error('Error deleting point:', error);
              // Handle error state or display error message
            });
          map.current.removeLayer(markerInstance);
        });
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
