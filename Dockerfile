# # Use official Python image
# FROM python:3.13-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Set working directory
# WORKDIR /app

# # Install dependencies
# COPY requirements.txt /app/
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# # Copy all project files
# COPY . /app/

# # Run migrations and start server
# CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
FROM python:3.13.3-slim

# Prevents .pyc files and enables real-time output logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install security patches and essential build tools
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y gcc build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /usr/src/app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Start command
CMD ["gunicorn", "codeeditor.wsgi:application", "--bind", "0.0.0.0:8000"]
