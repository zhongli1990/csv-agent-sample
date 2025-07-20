# Use Python 3.12 slim as base image
FROM python:3.12-slim

# Install system dependencies for pandas, matplotlib, and other tools
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libatlas-base-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    pkg-config \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy entrypoint script and set permissions
RUN chmod +x /app/start-agent.sh

# Expose port if needed (not strictly necessary for CLI app)
# EXPOSE 8000

# Default command to run the entrypoint script
CMD ["./start-agent.sh"] 