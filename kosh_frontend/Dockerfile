FROM node:22-slim

WORKDIR /app

COPY package*.json ./

# Install all dependencies (including dev deps)
RUN npm install

COPY ./kosh_frontend/. .

# Build Vite project
RUN npm run build

# Install tiny production static server
RUN npm install -g serve

# Cloud Run port
ENV PORT=8080
EXPOSE $PORT

# Serve Vite's dist folder
CMD ["serve", "-s", "dist", "-l", "8080"]
