# 🚀 FastAPI Clean Architecture Starter

โปรเจกต์ FastAPI ที่ใช้ Clean Architecture และ Domain-Driven Design (DDD) patterns พร้อมด้วย MongoDB (Beanie) และระบบ Modular ที่ง่ายต่อการขยาย

## ✨ คุณสมบัติเด่น

- 🏗️ **Clean Architecture** - แยกชั้นงานอย่างชัดเจน ง่ายต่อการดูแลรักษา
- 🔐 **ระบบ Authentication** - JWT Token และ Role-based Authorization
- 🗄️ **MongoDB + Beanie** - NoSQL Database ที่ใช้งานง่าย
- ⚡ **Auto Router Discovery** - ระบบค้นหา Router อัตโนมัติ
- 🛠️ **Development Tools** - CLI สำหรับสร้าง Module ใหม่
- 📝 **Type Safety** - TypeScript-like typing ใน Python
- 🧪 **Testing Ready** - โครงสร้างพร้อมสำหรับการทดสอบ

## 📁 โครงสร้างโปรเจกต์

```
fastapi-beanie-starter/
├── .env                      # ตัวแปรสิ่งแวดล้อม (Database URL, Secret Keys)
├── .env.sample              # ตัวอย่างไฟล์ Environment Variables
├── .gitignore               # ไฟล์ที่ไม่ต้องเก็บใน Git
├── pyproject.toml           # การจัดการ Dependencies ด้วย Poetry
├── poetry.lock              # Lock file สำหรับ Dependencies
├── poetry.toml              # การตั้งค่า Poetry
├── README.md                # คู่มือการใช้งาน (ไฟล์นี้)
│
├── .github/                 # GitHub Configuration
│   └── instructions/
│       └── fastapi.instructions.md  # คู่มือการพัฒนา FastAPI
│
├── apiapp/                 # โฟลเดอร์หลักของแอปพลิเคชัน
│   ├── __init__.py
│   ├── main.py              # จุดเริ่มต้นแอปพลิเคชัน
│   ├── run.py               # Script สำหรับรันเซิร์ฟเวอร์
│   │
│   ├── cmd/                 # Command Line Interface Components
│   │   └── __init__.py
│   │
│   ├── core/                # ชั้นธุรกิจและ Components ที่ใช้ร่วมกัน
│   │   ├── __init__.py
│   │   ├── base_repository.py  # Base Repository Pattern
│   │   ├── base_schemas.py     # Base Pydantic Schemas
│   │   ├── base_use_case.py    # Base Use Case Pattern
│   │   ├── config.py           # การตั้งค่าแอปพลิเคชัน
│   │   ├── exceptions.py       # Custom Exceptions
│   │   ├── http_error.py       # HTTP Error Handling
│   │   ├── router.py           # Base Router Configuration
│   │   ├── security.py         # JWT, Password Hashing
│   │   ├── validation_error.py # Validation Error Handling
│   │
│   ├── infrastructure/      # ชั้น Infrastructure และ External Services
│   │   ├── __init__.py
│   │   ├── database.py      # การเชื่อมต่อ MongoDB
│   │   └── gridfs.py        # การจัดเก็บไฟล์
│   │
│   ├── middlewares/         # FastAPI Middlewares
│   │   ├── __init__.py
│   │   ├── base.py          # จัดการ Middlewares ทั้งหมด
│   │   ├── cors.py          # CORS และการบีบอัด
│   │   ├── security.py      # กรอง User Agent
│   │   └── timing.py        # วัดประสิทธิภาพ
│   │
│   ├── utils/               # Utility Functions
│   │   ├── __init__.py
│   │   ├── logging.py       # การจัดการ Log
│   │   └── request_logs.py  # Log การ Request
│   │
│   └── modules/             # Feature Modules (Clean Architecture)
│       ├── __init__.py
│       ├── auth/            # โมดูลการเข้าสู่ระบบ
│       │   ├── __init__.py
│       │   └── schemas.py   # Pydantic Schemas สำหรับ Auth
│       │
│       ├── examples/        # โมดูลตัวอย่าง (สำหรับการทดสอบ)
│       │
│       ├── health/          # โมดูลตรวจสอบสถานะระบบ
│       │   ├── __init__.py
│       │   ├── router.py    # Health Check Endpoints
│       │   └── schemas.py   # Health Check Schemas
│       │
│       └── user/            # โมดูลจัดการผู้ใช้
│           ├── __init__.py
│           ├── model.py     # User Database Model
│           ├── repository.py # การเข้าถึงข้อมูล User
│           ├── router.py     # API Endpoints สำหรับ User
│           ├── schemas.py    # Pydantic Schemas สำหรับ User
│           └── use_case.py   # Business Logic สำหรับ User
│
├── cli/                     # CLI Tools สำหรับ Development
│   ├── __init__.py
│   ├── main.py              # CLI Entry Point
│   ├── create_module.py     # Module Generator
│   ├── README.md            # คู่มือ CLI
│   └── templates/           # Template Files สำหรับ Module Generation
│       ├── __init__.py.j2
│       ├── model.py.j2
│       ├── repository.py.j2
│       ├── router.py.j2
│       ├── schemas.py.j2
│       └── use_case.py.j2
│
├── docs/                    # Documentation
│   └── repository-usecase-pattern.md # คู่มือ Repository และ Use Case Pattern
│
└── scripts/                 # Development Scripts (deprecated - ใช้ CLI แทน)
    ├── init-admin           # สร้าง Admin User แรก
    ├── run-dev              # รันในโหมด Development
    ├── run-prod             # รันในโหมด Production
    └── README.md            # คู่มือ Scripts
```

## 💡 หลักการสำคัญ

### 🎯 Clean Architecture

- **Modules** ขึ้นอยู่กับ **Core** (import จาก `apiapp.core.*`)
- **Core** ไม่ขึ้นอยู่กับ **Modules**
- **Infrastructure** implement interfaces ที่กำหนดใน **Core**
- **Models** อยู่ภายใน module ของตัวเองเพื่อความเป็นระเบียบ

### 🔄 Dependency Injection

- ใช้ FastAPI's `Depends()` สำหรับ dependencies ทั้งหมด
- สร้าง dependency providers ใน `modules/{feature}/dependencies/`
- Inject use cases, repositories, และ services ผ่าน dependencies
- ไม่สร้าง object โดยตรงใน routers

### 📦 โครงสร้าง Module

แต่ละ feature module ต้องมีโครงสร้างตามนี้:

```
modules/{feature}/
├── __init__.py
├── model.py        # Database Model (Beanie Document)
├── schemas.py      # Pydantic schemas (DTOs)
├── repository.py   # ชั้นการเข้าถึงข้อมูล
├── use_case.py     # ชั้น Business Logic
└── router.py       # API endpoints
```

## 🚀 เริ่มต้นใช้งาน

### 📋 ความต้องการของระบบ

- Python 3.12+
- Poetry (สำหรับจัดการ dependencies)
- MongoDB (Local หรือ Cloud)

### ⚙️ การติดตั้ง

1. **Clone โปรเจกต์**

   ```bash
   git clone <repository-url>
   cd fastapi-beanie-starter
   ```

2. **ติดตั้ง Dependencies ด้วย Poetry**

   ```bash
   # ติดตั้ง Poetry (ถ้ายังไม่มี)
   curl -sSL https://install.python-poetry.org | python3 -

   # ติดตั้ง dependencies
   poetry install
   ```

3. **ตั้งค่า Environment Variables**

   ```bash
   # คัดลอกไฟล์ .env.example
   cp .env.example .env

   # แก้ไขไฟล์ .env ตามการตั้งค่าของคุณ
   nano .env
   ```

   ตัวอย่างไฟล์ `.env`:

   ```env
   # Database
   DATABASE_URL=mongodb://localhost:27017/fastapi_starter

   # Security
   SECRET_KEY=your-super-secret-key-here
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Environment
   ENVIRONMENT=development
   DEBUG=true
   ```

4. **รันแอปพลิเคชัน**

   ```bash
   # โหมด Development (ใหม่ - ใช้ CLI)
   poetry run velo app run dev
   
   # โหมด Production (ใหม่ - ใช้ CLI)
   poetry run velo app run prod
   
   # หรือใช้วิธีเดิม
   poetry run python apiapp/run.py
   ```

5. **เข้าถึง API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### 🎯 Quick Start - สร้าง API แรกของคุณ

1. **สร้าง Module ใหม่ด้วย CLI**

   ```bash
   # สร้าง products module แบบ interactive
   poetry run velo module create

   # หรือสร้างโดยระบุชื่อ
   poetry run velo module create products
   ```

2. **ไฟล์ที่สร้างขึ้นอัตโนมัติ:**

   - `modules/products/schemas.py` - กำหนดรูปแบบข้อมูล
   - `modules/products/repository.py` - จัดการการเข้าถึงฐานข้อมูล
   - `modules/products/use_case.py` - ใส่ Business Logic
   - `modules/products/router.py` - สร้าง API Endpoints
   - `modules/products/model.py` - กำหนด Database Model

3. **ระบบจะค้นหา Router อัตโนมัติ** - ไม่ต้องไปแก้ไขไฟล์ main.py

## 📖 ตัวอย่างการใช้งาน

### 🔐 Authentication

```python
# เข้าสู่ระบบ
POST /v1/auth/login
{
  "email": "user@example.com",
  "password": "password123"
}

# สมัครสมาชิก
POST /v1/auth/register
{
  "email": "newuser@example.com",
  "password": "password123",
  "full_name": "ชื่อผู้ใช้"
}
```

### 👤 User Management

```python
# ดูข้อมูลผู้ใช้
GET /v1/users/me
Authorization: Bearer <your-token>

# อัพเดทข้อมูล
PUT /v1/users/me
{
  "full_name": "ชื่อใหม่",
  "bio": "แนะนำตัว"
}
```

### ❤️ Health Check

```python
# ตรวจสอบสถานะระบบ
GET /v1/health
```

## 🛠️ Development Tools

### 🏗️ CLI - Module Generator

เครื่องมือ CLI ที่ทรงพลังสำหรับสร้าง FastAPI modules ใหม่ตามโครงสร้าง Clean Architecture:

```bash
# สร้าง module ใหม่ (Interactive mode)
poetry run velo module create

# สร้าง module โดยระบุชื่อ
poetry run velo module create products

# สร้างแบบ force overwrite
poetry run velo module create products --force

# ดูว่าจะสร้างไฟล์อะไรบ้าง (Dry run)
poetry run velo module create products --dry-run

# ดู modules ที่มีอยู่
poetry run velo module list

# ดู help
poetry run velo --help
poetry run velo module --help
```

**คุณสมบัติของ CLI:**

- ✅ **Auto Code Generation** - สร้างไฟล์ตาม Clean Architecture pattern
- ✅ **Interactive Mode** - ใช้งานง่ายด้วย prompt
- ✅ **Dry Run Mode** - ดูผลลัพธ์ก่อนสร้างไฟล์จริง
- ✅ **Force Overwrite** - เขียนทับไฟล์เดิมได้
- ✅ **Module Listing** - ดู modules ที่มีอยู่
- ✅ **Type Hints** - สร้าง code พร้อม type annotations

รายละเอียดเพิ่มเติม: [cli/README.md](cli/README.md)

### 🔧 CLI Commands (แนะนำ - ใหม่!)

```bash
# รันในโหมด Development (auto-reload)
poetry run velo app run dev

# รันในโหมด Production  
poetry run velo app run prod

# สร้าง Admin User แรก
poetry run velo admin create

# สร้าง Module ใหม่
poetry run velo module create products

# ดู Modules ที่มีอยู่
poetry run velo module list

# ดู Help
poetry run velo --help
```

### 🔧 Development Scripts (วิธีเดิม - ยังใช้ได้)

```bash
# รันในโหมด Development (auto-reload)
./scripts/run-dev

# รันในโหมด Production
./scripts/run-prod

# สร้าง Admin User แรก
./scripts/init-admin
```

> 💡 **แนะนำ**: ใช้ CLI commands (`poetry run velo`) แทน scripts เพื่อประสบการณ์ที่ดีกว่าและมี features เพิ่มเติม

## 📚 คู่มือการพัฒนา

### 🎨 การเขียน Code

1. **ใช้ Double Quotes** เป็นหลัก

   ```python
   # ✅ ถูกต้อง
   name = "John Doe"
   message = "Welcome to our API"

   # ❌ หลีกเลี่ยง
   name = 'John Doe'
   ```

2. **ใช้ Type Hints ทุกที่**

   ```python
   async def get_user(user_id: str) -> User | None:
       return await self.user_repository.find_by_id(user_id)
   ```

3. **ใช้ Dependency Injection**
   ```python
   @router.get("/users/me")
   async def get_current_user(
       current_user: User = Depends(get_current_active_user)
   ):
       return current_user
   ```

### 🚫 สิ่งที่ควรหลีกเลี่ยง

1. **ไม่ควร import model โดยตรงใน router**

   ```python
   # ❌ ไม่ถูกต้อง
   from apiapp.models.user_model import User
   user = await User.find_one({"email": email})

   # ✅ ถูกต้อง
   user = await user_use_case.get_by_email(email)
   ```

2. **ไม่ควรใส่ business logic ใน router**

   ```python
   # ❌ ไม่ถูกต้อง
   @router.post("/users")
   async def create_user(data: UserRequest):
       if len(data.password) < 8:
           raise HTTPException(400, "Password too short")

   # ✅ ถูกต้อง - ใส่ logic ใน use_case
   @router.post("/users")
   async def create_user(
       data: UserRequest,
       user_use_case: UserUseCase = Depends(get_user_use_case)
   ):
       return await user_use_case.create_user(data)
   ```

## 🧪 การทดสอบ

```bash
# รัน unit tests
poetry run pytest

# รัน tests พร้อม coverage
poetry run pytest --cov=apiapp

# รัน tests ในโหมด watch
poetry run pytest-watch
```

## 📝 การ Deploy

### 🐳 Docker

```bash
# Build image
docker build -t fastapi-app .

# Run container
docker run -p 8000:8000 fastapi-app
```

### ☁️ Cloud Deployment

โปรเจกต์นี้พร้อมสำหรับ deploy ไปยัง:

- **Heroku** - ใช้ไฟล์ `Procfile`
- **Railway** - Auto-detect Python
- **DigitalOcean App Platform** - ใช้ไฟล์ `.do/app.yaml`
- **AWS Lambda** - ด้วย Mangum adapter

## 🤝 การมีส่วนร่วม

1. Fork โปรเจกต์
2. สร้าง feature branch (`git checkout -b feature/amazing-feature`)
3. Commit การเปลี่ยนแปลง (`git commit -m 'Add amazing feature'`)
4. Push ไปยัง branch (`git push origin feature/amazing-feature`)
5. เปิด Pull Request

## 📄 License

โปรเจกต์นี้อยู่ภายใต้ MIT License - ดูรายละเอียดในไฟล์ [LICENSE](LICENSE)

## 🙋‍♂️ ต้องการความช่วยเหลือ?

- 📖 อ่านคู่มือเต็ม: [.github/instructions/fastapi.instructions.md](.github/instructions/fastapi.instructions.md)
- 🛠️ คู่มือ CLI: [cli/README.md](cli/README.md)
- 🐛 รายงานปัญหา: [GitHub Issues](https://github.com/your-repo/issues)
- 💬 หารือ: [GitHub Discussions](https://github.com/your-repo/discussions)

---

⭐ ถ้าโปรเจกต์นี้มีประโยชน์ กรุณา Star ให้ด้วยนะ!
