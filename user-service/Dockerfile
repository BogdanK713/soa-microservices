# Use lightweight Node image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Expose port and run app
EXPOSE 3000
CMD ["node", "src/index.js"]
