FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /app /app

# Hello world
# CMD ["echo", "Hello, World!"]

# dont exist after run
# ENTRYPOINT ["sh", "-c", "while true; do echo 'Hit CTRL+C'; sleep 60; done"]



CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
