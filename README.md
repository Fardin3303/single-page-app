# single-page-app
A single-page web application that includes a map interface

# Map Application

This project is a map application where users can add, edit, and delete points of interest on a map.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository:
    ```
    git clone <repository-url>
    cd project-root
    ```

2. Run the application:
    ```
    docker-compose up --build
    ```

The backend will be available at http://localhost:8000 and the frontend at http://localhost:3000.

## Endpoints

- `POST /token` - Get JWT token.
- `POST /users/` - Create a new user.
- `POST /points/` - Create a new point.
- `GET /points/` - Get all points.
- `DELETE /points/{point_id}` - Delete a point.

## Testing

Backend tests can be run using:


