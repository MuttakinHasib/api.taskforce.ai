# Taskforce

Taskforce HQ | Your intelligent AI-powered task management HQ.

## Quick Start with Make

This project includes a Makefile to simplify common operations. Here are some of the most useful commands:

```bash
# Start development environment
make dev

# Start production environment
make prod

# Stop containers
make down

# View help with all available commands
make help
```

## Docker Architecture

The application is containerized using Docker with two different configurations:

### Development Environment
```
┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │
│  Django (api)   │<────│   PostgreSQL    │
│  Dev Server     │     │   Database      │
│                 │     │                 │
└─────────────────┘     └─────────────────┘
       ^
       │
       v
┌─────────────────┐
│                 │
│    Host OS      │
│  Port 8000      │
│                 │
└─────────────────┘
```

### Production Environment
```
┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │
│     Nginx       │<────│  Django (api)   │
│  Web Server     │     │  + Gunicorn     │
│                 │     │                 │
└─────────────────┘     └─────────────────┘
       ^                        ^
       │                        │
       v                        v
┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │
│    Host OS      │     │   PostgreSQL    │
│  Port 80/443    │     │   Database      │
│                 │     │                 │
└─────────────────┘     └─────────────────┘
```

## Docker Setup

### Prerequisites

- Docker and Docker Compose installed on your system
- uv for Python dependency management (optional for local development)

### Development Setup

1. Copy the environment example file:

   ```bash
   cp .env.example .env.dev
   ```

2. Edit `.env.dev` with your desired configuration.

3. Build and start the development containers:

   ```bash
   make dev-build
   ```

4. Access the development server at <http://localhost:8000>

### Production Setup

1. Copy the environment example file:

   ```bash
   cp .env.example .env.prod
   ```

2. Edit `.env.prod` with secure production settings.

3. Build and start the production containers:

   ```bash
   make prod-build
   ```

4. The application will be served via Nginx on port 80/443.

### Working with Docker via Make

- Run Django management commands:
  
  ```bash
  make migrate         # Run migrations
  make makemigrations  # Create migrations
  make superuser       # Create superuser
  make shell           # Access Django shell
  ```

- Access the PostgreSQL database:
  
  ```bash
  make dbshell
  ```

- View logs:
  
  ```bash
  make logs      # Development logs
  make logs-prod # Production logs
  ```

- Check container status:
  
  ```bash
  make status      # Development status
  make status-prod # Production status
  ```

## Local Development (without Docker)

For local development without Docker, make sure you have:

1. Python 3.12+ installed
2. PostgreSQL running locally
3. uv installed

Then:

```bash
# Install dependencies
uv pip install -e .

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```
