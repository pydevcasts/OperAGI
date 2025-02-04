# Dockerfile for Vue.js Frontend
FROM node:alpine3.20

# Set environment variable for the application home
ENV APP_HOME=/frontend
RUN mkdir -p $APP_HOME
# Set the working directory
WORKDIR $APP_HOME

# Copy package.json and package-lock.json to the working directory
COPY ./vue-app/package*.json ./

# Install dependencies
RUN npm install 

# Copy the rest of the application code into the working directory
COPY ./vue-app ./

# Build the application
RUN npm run build

# Install serve globally
RUN npm install -g serve

# Expose the port the app runs on
EXPOSE 8080

# Command to serve the application
CMD ["npx", "serve", "-s", "dist"]
