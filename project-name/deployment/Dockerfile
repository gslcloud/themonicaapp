# Use an appropriate base image with a specific version tag
FROM python:3.9.6-alpine3.14

# Set the working directory
WORKDIR /app

# Copy requirements.txt file separately and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code into the container
COPY . .

# Switch to a non-root user for improved security
USER 1000

# Expose the necessary ports
EXPOSE 8000

# Define the command to start the application
CMD ["python", "app.py"]