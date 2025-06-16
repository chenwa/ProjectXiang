# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install MySQL client and other dependencies
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# No frontend build or copy steps needed, as the backend is now standalone.
# This Dockerfile only builds and runs the FastAPI backend.