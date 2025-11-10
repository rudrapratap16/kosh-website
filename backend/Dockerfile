# Lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port from environment variable
ENV PORT 8080
EXPOSE $PORT

# Start Gunicorn using the PORT variable
CMD exec gunicorn --bind 0.0.0.0:$PORT app:app
