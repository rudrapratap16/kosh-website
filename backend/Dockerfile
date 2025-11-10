# Lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory structure
COPY services/ ./services/
COPY app.py .
COPY config.py .

# Expose port from environment variable
ENV PORT 8080
EXPOSE $PORT

# Start Gunicorn using the PORT variable
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app