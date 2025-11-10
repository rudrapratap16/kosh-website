# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency file first (for better build caching)
COPY requirements.txt .

# Install dependencies (no cache for smaller image)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=8080

# Expose the port Cloud Run expects
EXPOSE 8080

# Run the Flask app
CMD ["python", "app.py"]
