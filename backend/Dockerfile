# Dockerfile for Django Backend
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
USER root
# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt
# Copy the project files
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "app:app", "--workers", "3", "--worker-class", "sync", "--bind", "0.0.0.0:8000"]