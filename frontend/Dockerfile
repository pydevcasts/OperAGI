# Use a smaller base image for production
FROM node:18-alpine

# Set environment variables
ENV APP_HOME=/frontend
ENV NODE_ENV=production

# Create app directory
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# Install dependencies (using npm ci for reproducible builds)
COPY ./vue-app/package*.json ./
RUN npm ci --only=production

# Copy the rest of the application code
COPY ./vue-app ./

# Build the application
RUN npm run build

# Install serve globally to serve the static files
RUN npm install -g serve

# Expose the port the app runs on
EXPOSE 3000

# Command to serve the application
CMD ["serve", "-s", "dist", "-l", "3000"]