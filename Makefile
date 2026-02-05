.PHONY: help build up down logs restart clean setup dev prod

# Default target
help:
	@echo "EventSquare Docker Management"
	@echo "=============================="
	@echo ""
	@echo "Setup Commands:"
	@echo "  make setup      - Initial setup (copy .env, create directories)"
	@echo "  make build      - Build all Docker images"
	@echo ""
	@echo "Development Commands:"
	@echo "  make dev        - Start in development mode"
	@echo "  make dev-logs   - View development logs"
	@echo "  make dev-down   - Stop development containers"
	@echo ""
	@echo "Production Commands:"
	@echo "  make prod       - Start in production mode"
	@echo "  make up         - Start all services"
	@echo "  make down       - Stop all services"
	@echo "  make restart    - Restart all services"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make logs       - View logs (all services)"
	@echo "  make ps         - Show container status"
	@echo "  make clean      - Remove containers and volumes"
	@echo "  make prune      - Clean up Docker system"
	@echo ""
	@echo "Database Commands:"
	@echo "  make db-shell   - Access MongoDB shell"
	@echo "  make db-backup  - Backup database"
	@echo "  make redis-cli  - Access Redis CLI"
	@echo ""
	@echo "Application Commands:"
	@echo "  make init-admin - Initialize admin user"
	@echo "  make backend-shell - Access backend shell"
	@echo "  make frontend-shell - Access frontend shell"

# Setup
setup:
	@echo "Setting up EventSquare..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file - PLEASE UPDATE WITH YOUR VALUES!"; \
	fi
	@mkdir -p nginx/ssl nginx/conf.d
	@echo "Setup complete!"

# Build
build:
	docker-compose build

build-no-cache:
	docker-compose build --no-cache

# Development
dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
	@echo "Development environment started!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:9000/docs"

dev-logs:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f

dev-down:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

# Production
prod: build
	docker-compose up -d
	@echo "Production environment started!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:9000/docs"

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

# Logs
logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-worker:
	docker-compose logs -f worker

# Status
ps:
	docker-compose ps

# Database
db-shell:
	docker-compose exec mongodb mongosh -u admin -p

db-backup:
	@mkdir -p backups
	docker-compose exec mongodb mongodump --out=/data/backup-$(shell date +%Y%m%d-%H%M%S)
	@echo "Backup created in MongoDB container"

redis-cli:
	docker-compose exec redis redis-cli

# Application
init-admin:
	docker-compose exec backend poetry run python scripts/init-admin

backend-shell:
	docker-compose exec backend bash

frontend-shell:
	docker-compose exec frontend sh

# Cleanup
clean:
	docker-compose down -v
	@echo "Containers and volumes removed"

prune:
	docker system prune -af --volumes
	@echo "Docker system cleaned"

# Health check
health:
	@echo "Checking service health..."
	@curl -f http://localhost:9000/docs || echo "Backend: DOWN"
	@curl -f http://localhost:3000 || echo "Frontend: DOWN"

# Update
update: build down up
	@echo "Application updated!"

# Scale
scale-workers:
	docker-compose up -d --scale worker=3
