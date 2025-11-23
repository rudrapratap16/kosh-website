# Use a lightweight Node image
FROM node:18-slim

# Set working directory
WORKDIR /app

# Copy dependency files first (improves caching)
COPY package*.json ./

# Install dependencies
RUN npm install --omit=dev

# Copy the full project
COPY . .

# Build the React app
RUN npm run build

# Install a lightweight static server
RUN npm install -g serve

# Cloud Run provides PORT, but 8080 is recommended
ENV PORT=8080
EXPOSE $PORT

# Start the static server on Cloud Run port
CMD ["serve", "-s", "build", "-l", "8080"]
