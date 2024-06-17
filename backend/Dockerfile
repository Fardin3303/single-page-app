FROM python:3.10-slim

# Install GCC, libpq-dev, and other dependencies
RUN apt-get update && \
    apt-get install -y build-essential gcc libpq-dev 

WORKDIR /backend

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /backend

RUN echo "backend image built successfully!"
