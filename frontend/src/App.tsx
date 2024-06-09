import React, { useState, useEffect } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMapEvents,
} from "react-leaflet";
import { v4 as uuidv4 } from "uuid";
import "leaflet/dist/leaflet.css";

const App: React.FC = () => {
  const [markers, setMarkers] = useState<any[]>([]);
  const [description, setDescription] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);

  // Function to handle user login
  const handleLogin = () => {
    // Call your authentication API endpoint here
    // Upon successful authentication, set isLoggedIn to true
    setIsLoggedIn(true);
  };

  // Function to handle user logout
  const handleLogout = () => {
    // Perform any necessary cleanup (e.g., clearing local storage)
    setIsLoggedIn(false);
  };

  useEffect(() => {
    // Check if the user is already logged in (e.g., from previous session)
    // If the user is logged in, set isLoggedIn to true
    const token = localStorage.getItem("token");
    if (token) {
      setIsLoggedIn(true);
    }
  }, []);

  const AddMarker = () => {
    useMapEvents({
      click(e) {
        const newMarker = {
          id: uuidv4(),
          position: e.latlng,
          description: "",
          createdAt: new Date().toISOString(),
          userId: "current-user-id",
        };
        setMarkers((prevMarkers) => [...prevMarkers, newMarker]);
      },
    });
    return null;
  };

  const handleDeleteMarker = (id: string) => {
    setMarkers((prevMarkers) =>
      prevMarkers.filter((marker) => marker.id !== id)
    );
  };

  return (
    <>
      {isLoggedIn ? (
        <>
          <button onClick={handleLogout}>Logout</button>
          <MapContainer
            center={[51.505, -0.09]}
            zoom={13}
            style={{ height: "100vh", width: "100%" }}
          >
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            <AddMarker />
            {markers.map((marker) => (
              <Marker key={marker.id} position={marker.position}>
                <Popup>
                  <div>
                    <textarea
                      value={marker.description}
                      onChange={(e) => {
                        const newDescription = e.target.value;
                        setMarkers((prevMarkers) =>
                          prevMarkers.map((m) =>
                            m.id === marker.id
                              ? { ...m, description: newDescription }
                              : m
                          )
                        );
                      }}
                    />
                    <button onClick={() => handleDeleteMarker(marker.id)}>
                      Delete
                    </button>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </>
      ) : (
        <LoginForm onLogin={handleLogin} />
      )}
    </>
  );
};

// Login form component
const LoginForm: React.FC<{ onLogin: () => void }> = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Call your authentication API endpoint here with username and password
    // Upon successful login, call the onLogin callback
    onLogin();
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default App;
  
  // In the above code, we have created a simple React application that allows users to add markers on a map. The user can add a marker by clicking on the map, and each marker has a description that can be edited. The user can also delete a marker by clicking on the delete button in the marker popup. 
  // The application also includes a simple login form that allows users to log in. Once the user is logged in, they can add and delete markers. The login state is stored in the  isLoggedIn  state variable, which is set to  true  when the user is logged in. 
  // The  handleLogin  function is called when the user logs in, and the  handleLogout  function is called when the user logs out. These functions can be used to perform any necessary actions when the user logs in or logs out, such as calling an authentication API endpoint or clearing local storage. 
  // The  LoginForm  component is a simple form that allows users to enter their username and password and submit the form to log in. When the form is submitted, the  handleSubmit  function is called, which can be used to call an authentication API endpoint with the username and password. Upon successful login, the  onLogin  callback is called to set the  isLoggedIn  state to  true . 

