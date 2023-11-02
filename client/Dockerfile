# Use node as the base image
FROM node:18

LABEL version="1.0"

# Set the working directory
WORKDIR /xweeter

# Install the dependencies
COPY . .
RUN npm install

# Build the app
RUN npm run build

# Set the port
EXPOSE 4173

# Set the command to run the app
CMD ["npm", "run", "preview"]