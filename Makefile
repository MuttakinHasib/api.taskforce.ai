.PHONY: help dev prod down migrate superuser shell logs clean test static build-dev build-prod restart db

# Variables
DEV_COMPOSE = docker compose -f docker-compose.dev.yml
PROD_COMPOSE = docker compose -f docker-compose.prod.yml
SERVICE = api
POSTGRES_USER ?= postgres
POSTGRES_DB ?= taskforce_dev

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: ## Start development environment
	$(DEV_COMPOSE) up -d

dev-build: ## Rebuild and start development environment
	$(DEV_COMPOSE) up -d --build

prod: ## Start production environment
	$(PROD_COMPOSE) up -d

prod-build: ## Rebuild and start production environment
	$(PROD_COMPOSE) up -d --build

down: ## Stop containers
	$(DEV_COMPOSE) down

down-prod: ## Stop production containers
	$(PROD_COMPOSE) down

restart: ## Restart development containers
	$(DEV_COMPOSE) restart

restart-prod: ## Restart production containers
	$(PROD_COMPOSE) restart

migrate: ## Run Django migrations
	$(DEV_COMPOSE) exec $(SERVICE) python manage.py migrate

makemigrations: ## Create Django migrations
	$(DEV_COMPOSE) exec $(SERVICE) python manage.py makemigrations

superuser: ## Create Django superuser
	$(DEV_COMPOSE) exec $(SERVICE) python manage.py createsuperuser

shell: ## Access Django shell
	$(DEV_COMPOSE) exec $(SERVICE) python manage.py shell

dbshell: ## Access database shell
	$(DEV_COMPOSE) exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

db: ## Start only the database container
	$(DEV_COMPOSE) up -d db

logs: ## View development logs
	$(DEV_COMPOSE) logs -f

logs-api: ## View only API logs
	$(DEV_COMPOSE) logs -f $(SERVICE)

logs-prod: ## View production logs
	$(PROD_COMPOSE) logs -f

logs-prod-api: ## View only production API logs
	$(PROD_COMPOSE) logs -f $(SERVICE)

test: ## Run tests
	$(DEV_COMPOSE) exec $(SERVICE) python manage.py test

coverage: ## Run tests with coverage
	$(DEV_COMPOSE) exec $(SERVICE) coverage run --source='.' manage.py test
	$(DEV_COMPOSE) exec $(SERVICE) coverage report

static: ## Collect static files
	$(DEV_COMPOSE) exec $(SERVICE) python manage.py collectstatic --no-input

lint: ## Run linting
	$(DEV_COMPOSE) exec $(SERVICE) black .
	$(DEV_COMPOSE) exec $(SERVICE) isort .

clean: ## Remove all containers, networks, and volumes
	docker system prune -af --volumes

status: ## Check container status
	$(DEV_COMPOSE) ps

status-prod: ## Check production container status
	$(PROD_COMPOSE) ps

create-app: ## Create a new Django app (usage: make create-app name=app_name)
	$(DEV_COMPOSE) exec $(SERVICE) python manage.py startapp $(name)
	@echo "App $(name) created in the 'apps' directory" 