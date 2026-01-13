## Project Structure

Use a modular and organized project structure.

```
project/
│-- app/
│   ├── __init__.py                 # Entry point
│   ├── core                        # Core dependency
│   │   ├── __init__.py               
│   │   ├── config.py               # Configuration settings
│   │   ├── dependencies.py         # Dependency injection
│   ├── models/                     # ORM models (MongoEngine, SQLAlchemy, etc.)
│   │   ├── __init__.py
│   │   ├── user_model.py
│   │   ├── product_model.py
│   ├── schemas/                    # Pydantic models
│   │   ├── __init__.py
│   │   ├── user_schema.py
│   │   ├── product_schema.py
│   ├── routes/                     # API routes
│   │   ├── __init__.py
│   │   ├── v1
│   │   │   ├── __init__.py
│   │   │   ├── user_route.py
│   │   │   ├── product_route.py
│   ├── services/                   # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── product_service.py
│   ├── repositories/               # Database queries
│   │   ├── __init__.py
│   │   ├── user_repo.py
│   │   ├── product_repo.py
│   ├── middlewares/                # Custom middlewares
│   ├── utils/                      # Utility functions
│   ├── tests/                      # Unit and integration tests
├── scripts/                        # Shell scripts
│-- .env                            # Environment variables
│-- Dockerfile                      # Docker setup
│-- pyproject.toml                  # Python Packages Management
│-- .gitignore                      # Git Ignore
```