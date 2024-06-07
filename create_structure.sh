#!/bin/bash

# # Base directory
# mkdir -p single-page-app

# Backend directories and files
mkdir -p backend/app/routers
mkdir -p backend/tests
mkdir -p backend/alembic/versions

touch backend/app/__init__.py
touch backend/app/main.py
touch backend/app/models.py
touch backend/app/schemas.py
touch backend/app/crud.py
touch backend/app/dependencies.py
touch backend/app/database.py
touch backend/app/routers/__init__.py
touch backend/app/routers/auth.py
touch backend/app/routers/points.py

touch backend/tests/test_auth.py
touch backend/tests/test_points.py

touch backend/Dockerfile
touch backend/requirements.txt
touch backend/alembic/env.py

# Frontend directories and files
mkdir -p frontend/public
mkdir -p frontend/src/components
mkdir -p frontend/src/pages

touch frontend/src/App.tsx
touch frontend/src/index.tsx

touch frontend/Dockerfile
touch frontend/package.json
touch frontend/tsconfig.json

# Root-level files
touch docker-compose.yml
touch README.md

echo "Directory structure and files created successfully."
