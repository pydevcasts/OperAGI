# Dockerfile for Django Backend
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
ENV APP_HOME=/app
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

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
CMD ["gunicorn", "conf.wsgi:application", "--workers", "3", "--worker-class", "sync", "--bind", "0.0.0.0:8000"]
