## 📁 โครงสร้างโปรเจกต์

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

## 🚀 คุณสมบัติหลัก

- **FastAPI**: Framework สำหรับการสร้าง API ที่รวดเร็ว และรองรับ async/await
- **Beanie**: Asynchronous ODM บน MongoDB ที่ใช้ Pydantic Model
- แบ่งโครงสร้างโค้ดตามหน้าที่ เช่น `models`, `schemas`, `routes`, `services`, `repositories`
- รองรับการจัดการ Configuration ผ่าน Environment Variables
- มีชุดตัวอย่าง API พร้อมทดสอบอัตโนมัติด้วย **Pytest**

## ⚙️ การติดตั้งและใช้งาน

1. **Clone โปรเจกต์**
    
    ```
    git clone https://github.com/importstar/fastapi-beanie-starter.git
    cd fastapi-beanie-starter
    ```
    
2. **สร้าง Virtual Environment และติดตั้ง dependencies**
    
    ```
    python -m venv .venv
    source .venv/bin/activate
    pip install poetry
    poetry install
    ```
    
3. **คัดลอกไฟล์ `.env`**
    
    ```
    cp .env.example .env
    ```
    
    ปรับค่าตัวแปร เช่น:
    
    ```
    APP_ENV="dev"
    DEBUG=True
    TITLE="IMPs FastAPI"
    VERSION="0.1.0"
    DATABASE_URI="mongodb://localhost:27017/eventsquaredb"
    SECRET_KEY="Th1s_1s_my_3xampl3_0f_s3cr3t_k3y_0123456789"
    ```
    
4. **รันเซิร์ฟเวอร์**
    
    ```
    ./script/run-dev
    ```
    
5. **เข้าใช้งาน API Docs**
เปิดเว็บเบราว์เซอร์ไปที่: `http://127.0.0.1:9000/docs`