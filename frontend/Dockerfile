# Use the official Node.js image as the base image
FROM node:20

# Set the working directory
WORKDIR /

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire project
COPY . .

# Build the Svelte application
RUN npm run build

# Use a lightweight Node.js image for serving the built app
FROM node:lts-bullseye-slim AS production

# Set the working directory
WORKDIR /

# Copy the built app from the previous stage
COPY --from=0 /dist /dist

# Install serve to serve the built app
RUN npm install -g serve

# Expose the port the app will run on
EXPOSE 3000

# Start the app
CMD ["serve", "-s", "dist", "-l", "3000"]