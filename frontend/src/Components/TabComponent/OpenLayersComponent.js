
// // This component is can be used to display an OpenLayers map with markers that can be added, updated and deleted.
// //Can be added to the TabComponent.js file to display the OpenLayers map.

// import React, { useEffect, useState, useRef } from 'react';
// import 'ol/ol.css';
// import Map from 'ol/Map';
// import View from 'ol/View';
// import TileLayer from 'ol/layer/Tile';
// import OSM from 'ol/source/OSM';
// import Feature from 'ol/Feature';
// import Point from 'ol/geom/Point';
// import { fromLonLat } from 'ol/proj';
// import Overlay from 'ol/Overlay';
// import VectorLayer from 'ol/layer/Vector';
// import VectorSource from 'ol/source/Vector';
// import { Icon, Style } from 'ol/style';
// import { defaults as defaultControls, ScaleLine } from 'ol/control';
// import { getPoints, createPoint, updatePoint, deletePoint } from '../../api/api';
// import { createUser, getTokenForUser } from "../../api/AuthService";

// let userToken = '';

// const initializeUser = async () => {
//   try {
//     const userData = {
//       username: prompt("Please enter your username", "Username"),
//       password: prompt("Please enter your password", "Password"),
//     };
//     if (!userData.username || !userData.password) {
//       throw new Error('Username and password are required');
//     }
//     const user = await createUser(userData);
//     console.log('User created successfully:', user);
//     const tokenResponse = await getTokenForUser(userData.username, userData.password);
//     console.log('Token received successfully:', tokenResponse);
//     userToken = tokenResponse.access_token;
//   } catch (error) {
//     console.error('Error initializing user:', error);
//     // Handle error state or display error message
//   }
// };

// initializeUser();

// const OpenLayersComponent = () => {
//   const mapContainerRef = useRef(null);
//   const map = useRef(null);
//   const popup = useRef(null);

//   const [markers, setMarkers] = useState([]);

//   useEffect(() => {
//     getPoints()
//       .then((points) => {
//         console.log('Points fetched successfully:', points);
//         setMarkers(points.map((point) => ({
//           id: point.id,
//           lat: parseFloat(point.latitude),
//           lon: parseFloat(point.longitude),
//           description: point.description,
//         })));
//       })
//       .catch((error) => {
//         console.error('Error fetching points:', error);
//         // Handle error state or display error message
//       });
//   }, []);

//   useEffect(() => {
//     map.current = new Map({
//       target: mapContainerRef.current,
//       layers: [
//         new TileLayer({
//           source: new OSM(),
//         }),
//       ],
//       controls: defaultControls().extend([
//         new ScaleLine(),
//       ]),
//       view: new View({
//         center: fromLonLat([24.926, 60.227]),
//         zoom: 12,
//       }),
//     });

//     map.current.on('click', (event) => {
//       const coordinate = event.coordinate;
//       const [lon, lat] = fromLonLat(coordinate);
//       const description = prompt("Please enter the description for the point", "Description");

//       if (!description) {
//         alert("Description is required");
//         return;
//       }

//       const pointData = {
//         description: description,
//         latitude: lat.toString(),
//         longitude: lon.toString(),
//         created_at: new Date().toISOString(),
//       };

//       createPoint(pointData, userToken)
//         .then((data) => {
//           console.log('Point created successfully:', data);
//           const newMarker = { id: data.id, lat, lon, description };
//           setMarkers((prevMarkers) => [...prevMarkers, newMarker]);
//           addMarker(newMarker);
//         })
//         .catch((error) => {
//           console.error('Error creating point:', error);
//         });
//     });

//     return () => {
//       map.current.setTarget(null);
//     };
//   }, []);

//   useEffect(() => {
//     markers.forEach((marker) => {
//       addMarker(marker);
//     });
//   }, [markers]);

//   const addMarker = (marker) => {
//     const iconStyle = new Style({
//       image: new Icon({
//         src: 'https://leafletjs.com/examples/custom-icons/leaf-red.png',
//         anchor: [0.5, 1],
//         scale: 0.5,
//       }),
//     });

//     const feature = new Feature({
//       geometry: new Point(fromLonLat([marker.lon, marker.lat])),
//     });

//     feature.setStyle(iconStyle);

//     const overlay = new Overlay({
//       element: createPopup(marker),
//       positioning: 'bottom-center',
//       stopEvent: false,
//       offset: [0, -50],
//     });

//     map.current.addOverlay(overlay);

//     feature.on('click', (evt) => {
//       overlay.setPosition(evt.coordinate);
//     });

//     const vectorSource = new VectorSource({
//       features: [feature],
//     });

//     const vectorLayer = new VectorLayer({
//       source: vectorSource,
//     });

//     map.current.addLayer(vectorLayer);
//   };

//   const createPopup = (marker) => {
//     const popupContent = document.createElement('div');
//     popupContent.innerHTML = `
//       <b>Marker at</b><br>Lat: ${marker.lat}<br>Lon: ${marker.lon}<br>
//       <input type="text" id="desc-${marker.id}" class="marker-input" placeholder="Enter description" value="${marker.description}" />
//       <button id="update-${marker.id}" class="marker-update-btn">Update</button>
//       <button id="delete-${marker.id}" class="marker-delete-btn">Delete</button>
//     `;

//     popup.current = new Overlay({
//       element: popupContent,
//       positioning: 'bottom-center',
//       stopEvent: false,
//       offset: [0, -50],
//     });

//     map.current.addOverlay(popup.current);

//     popupContent.querySelector(`#update-${marker.id}`).addEventListener('click', () => {
//       const newDescription = popupContent.querySelector(`#desc-${marker.id}`).value;
//       updateMarkerDescription(marker.id, newDescription);
//       updatePoint(marker.id, newDescription, userToken)
//         .then((updatedPoint) => {
//           console.log('Point updated successfully:', updatedPoint);
//         })
//         .catch((error) => {
//           console.error('Error updating point:', error);
//         });
//       popup.current.setPosition(undefined);
//     });

//     popupContent.querySelector(`#delete-${marker.id}`).addEventListener('click', () => {
//       setMarkers((prevMarkers) => prevMarkers.filter((m) => m.id !== marker.id));
//       deletePoint(marker.id, userToken)
//         .then((deletedPoint) => {
//           console.log('Point deleted successfully:', deletedPoint);
//         })
//         .catch((error) => {
//           console.error('Error deleting point:', error);
//         });
//       popup.current.setPosition(undefined);
//     });

//     return popupContent;
//   };

//   const updateMarkerDescription = (markerId, newDescription) => {
//     setMarkers((prevMarkers) =>
//       prevMarkers.map((marker) =>
//         marker.id === markerId ? { ...marker, description: newDescription } : marker
//       )
//     );
//   };

//   return (
//     <div>
//       <div className="map-container" ref={mapContainerRef} style={{ height: '80vh', width: '100%' }} />
//     </div>
//   );
// };

// export default OpenLayersComponent;
