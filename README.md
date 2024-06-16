Points of Interest Web Application
----------------------------------

This is a single-page web application demo that allows users to interact with a map interface to add, edit, and delete points of interest (POIs). Each POI consists of a marker on the map accompanied by a free-text description. Users must be authenticated to create and edit POIs, and they can only edit or delete the POIs they have created.

The application is built using a modern tech stack, with the backend developed using FastAPI and Python, a PostgreSQL database for storing POI data and user information, and a React frontend to create a dynamic single-page application. The application is containerized using Docker for easy deployment and scalability.

### Prerequisites

*   **Docker**: Install Docker from the [official website](https://www.docker.com/get-started).


### Features

*   **Map Interface**: Utilizes [Leaflet](https://leafletjs.com/) to display an interactive map.
    
*   **Points of Interest**: Users can add new POIs by placing markers on the map and providing a description. They can edit or delete their own POIs.
    
*   **Authentication and Authorization**:
    
    *   Users must register and log in to the system.
        
    *   Authenticated users can view all POIs but can only modify the ones they created.
        
*   **Technology Stack**:
    
    *   **Backend**: Developed using **Python** with **FastAPI**, providing a RESTful API.
        
    *   **Database**: **PostgreSQL** for storing POI data and user information.
        
    *   **Frontend**: Built with **React** to create a dynamic single-page application.
        
    *   **Containerization**: Docker used for packaging the application into containers for easy deployment and scalability.
        

### Tech Stack

*   **Backend**: FastAPI, Python
    
*   **Frontend**: React
    
*   **Database**: PostgreSQL
    
*   **Mapping Library**: OpenLayers
    

### Setup Instructions

To run this application locally, follow these steps:

1.  Clone the repository:
    
    ```bash
    git clone git@github.com:Fardin3303/single-page-app.git
    ```

2.  Navigate to the project directory:
    
    ```bash
    cd single-page-app

3. Run the following command to build the docker image:
    
    ```bash
    docker-compose up --build

Fronend will be running on `http://localhost:3000` and backend will be running on `http://localhost:8000`.

### Endpoints

- `POST /token` - Get JWT token.
- `POST /users/` - Create a new user.
- `POST /points/` - Create a new point.
- `GET /points/` - Get all points.
- `DELETE /points/{point_id}` - Delete a point.
- `PUT /points/{point_id}` - Update a point.

### Testing

To run the unit tests, execute the following command:

```bash
cd backend

pytest tests/unit_tests
```