# Alex Auth
Simple auth provider with a frontend.

## Usage
This project needs a .env file. Just rename the `example.env` file to .env an configure the keys as you see fit.

You have two options to run this project. Docker is highly recommended.

### Docker
If you have [Docker installed](https://docs.docker.com/engine/install/), you can run this project using the cli command `docker compose up -d` in the root directory.

### Python
If you don't want to use Docker but have Python installed, you can run this project using the commands `python auth-service/main.py` and `python frontend/main.py` in two separate shells.