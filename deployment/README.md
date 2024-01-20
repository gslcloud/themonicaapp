
# Deployment Guide

This guide provides instructions for deploying the platform centered around Monica.

## Prerequisites
- Python 3.9
- Pipenv version 2021.11.15 or later

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/project-name.git
   cd project-name
   ```

2. Install project dependencies:
   ```
   pipenv install
   ```

3. Activate the virtual environment:
   ```
   pipenv shell
   ```

4. Run the development server:
   ```
   pipenv run start
   ```

5. Access the application at http://localhost:8000

## Configuration

The following environment variables should be configured:

- `DATABASE_URL`: The URL of the PostgreSQL database.
- `REDIS_URL`: The URL of the Redis server.
- `STRIPE_API_KEY`: The API key for integrating with Stripe.

Consider creating a dotenv (.env) file in the project root directory to manage your environment variables. This file should not be committed to version control for security reasons. You can include the required environment variables in the dotenv file and load them using a library like python-decouple or dotenv in your application.

## Database Migration

Before starting the server, you need to run the database migration to set up the database schema. Use the following command:
```
pipenv run alembic upgrade head
```
This command will apply any pending database migrations.

## Deployment to Heroku

1. Create a new Heroku app:
   ```
   heroku create your-app-name
   ```

2. Set the necessary environment variables:
   ```
   heroku config:set DATABASE_URL=your-database-url
   heroku config:set REDIS_URL=your-redis-url
   heroku config:set STRIPE_API_KEY=your-stripe-api-key
   ```

3. Deploy the app:
   ```
   git push heroku main
   ```

4. Open the app in your browser:
   ```
   heroku open
   ```

Make sure to follow these instructions to deploy the platform successfully. If you have any questions or need further assistance, please don't hesitate to reach out.