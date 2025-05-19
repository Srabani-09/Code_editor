FROM python:3.13.3-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y gcc build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /usr/src/app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project source code
COPY . .

# Use Render's startCommand instead of CMD here, so omit CMD in Dockerfile
# CMD ["gunicorn", "codeeditor.wsgi:application", "--bind", "0.0.0.0:8000"]

