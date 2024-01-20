#!/bin/bash

# Load environment variables
source .env

# Log start message
echo "Deployment process initiated..."

# Validate required environment variables
if [[ -z "$DATABASE_URL" ]]; then
  echo "Error: DATABASE_URL environment variable is not set."
  exit 1
fi

# Log environment variables
echo "DATABASE_URL: $DATABASE_URL"
# Add more environment variables as necessary

# Front-end build
echo "Building front-end assets..."
cd frontend
npm install
npm run build
cd ..

# Database migration
echo "Running database migrations..."
python manage.py db upgrade

# Restart application server
echo "Restarting application server..."
sudo systemctl restart $YOUR_APP_SERVICE_NAME

# Log completion message
echo "Deployment process completed successfully."