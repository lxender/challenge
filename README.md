# User Management System Challenge
Simple user management system with a frontend.

There are two user-tiers: normal and admin users. By default, the first user to be registered, is an admin user. The id of the admin user can be changed in the .env file.

Additionally, there are two dashboards: a self-service dashboard for users and an admin dashboard managing users.

## Usage
This project needs a .env file. Just rename the `example.env` file to .env an configure the keys as you see fit.

You have two options to run this project. Docker is highly recommended.

When the project is up and running, the frontend is available at http://localhost:5000/

### Docker
If you have [Docker installed](https://docs.docker.com/engine/install/), you can run this project using the cli command `docker compose up` in the root directory.

### Python
If you don't want to use Docker but have Python installed, you can run this project using the commands `python auth-service/main.py` and `python frontend/main.py` in two separate shells.

## Testing
This project has integration tests for the API endpoints.

They can be run directly with `pytest` (or `python -m pytest` if you're running into issues) or `docker compose -f docker-compose.test.yml up --build`
