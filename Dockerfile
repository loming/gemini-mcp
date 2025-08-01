FROM node:18-alpine

WORKDIR /app

# Install gemini-cli globally (breaking system packages as this is a container)
RUN npm install -g @google/gemini-cli

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Expose port
EXPOSE 13001

# Start the application
CMD ["npm", "run", "start"]
