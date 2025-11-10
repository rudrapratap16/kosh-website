# Lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory structure
COPY utils/ ./utils/
COPY dashboard.py .

# Expose port from environment variable
ENV PORT 8080
EXPOSE $PORT

# Start stramlit using the PORT variable
CMD streamlit run dashboard.py --server.port=$PORT