# Velo CLI - FastAPI Beanie Starter CLI Tools

เครื่องมือ Command Line Interface สำหรับจัดการโปรเจกต์ FastAPI Beanie Starter

## 🚀 การติดตั้ง

CLI นี้ติดตั้งมาพร้อมกับโปรเจกต์แล้ว สามารถใช้งานผ่าน Poetry:

```bash
# ใช้งาน CLI ผ่าน poetry script
poetry run velo

# หรือหลังจาก activate virtual environment
velo
```

## 📋 คำสั่งที่มีให้ใช้

### Module Management

#### สร้าง Module ใหม่

```bash
# สร้าง module ใหม่แบบ interactive
poetry run velo module

# สร้าง module โดยระบุชื่อ
poetry run velo module create products

# สร้างแบบ force overwrite (เขียนทับไฟล์เดิม)
poetry run velo module create products --force

# ดูว่าจะสร้างไฟล์อะไรบ้าง (Dry run - ไม่สร้างไฟล์จริง)
poetry run velo module create products --dry-run

# ดู modules ที่มีอยู่
poetry run velo module list

# ดู help สำหรับ module commands
poetry run velo module --help
```

### ตัวอย่างการใช้งาน

```bash
# 1. สร้าง products module
poetry run velo module create products

# 2. สร้าง orders module แบบ force
poetry run velo module create orders --force

# 3. ดู modules ทั้งหมด
poetry run velo module list

# 4. ดูว่า posts module จะสร้างไฟล์อะไรบ้าง (ไม่สร้างจริง)
poetry run velo module create posts --dry-run
```

## 📁 ไฟล์ที่ CLI จะสร้างให้

เมื่อสร้าง module ใหม่ด้วยคำสั่ง `velo module create <module_name>` ระบบจะสร้างไฟล์เหล่านี้:

### Module Structure

```
apiapp/modules/{module_name}/
├── __init__.py          # Package initialization
├── schemas.py           # Pydantic schemas (DTOs) สำหรับ validation
├── repository.py        # Data access layer สำหรับเข้าถึง database
├── use_case.py          # Business logic layer สำหรับ business rules
└── router.py            # API endpoints สำหรับ HTTP requests
```

### Database Model

```
apiapp/models/
└── {module_name}_model.py   # Beanie document model สำหรับ database
```

## 🎯 หลักการสำคัญ

### Clean Architecture Pattern

ไฟล์ที่ CLI สร้างขึ้นจะเป็นไปตามหลัก Clean Architecture:

1. **schemas.py** - ชั้น Presentation (DTOs)
2. **router.py** - ชั้น Interface Adapters (API Endpoints)
3. **use_case.py** - ชั้น Application/Business Logic
4. **repository.py** - ชั้น Infrastructure (Data Access)
5. **{name}\_model.py** - ชั้น Entity (Database Models)

### Auto Router Discovery

Router ที่สร้างขึ้นจะถูกค้นหาและโหลดอัตโนมัติโดยระบบ ไม่ต้องไปแก้ไขไฟล์ `main.py`

## 🔧 คำสั่ง CLI ทั้งหมด

```bash
# ดู help หลัก
poetry run velo --help

# ดู help สำหรับ module commands
poetry run velo module --help

# ดู version
poetry run velo --version
```

## 💡 Tips และ Best Practices

1. **ใช้ชื่อ module เป็น singular form** (เช่น `product` แทน `products`)
2. **ชื่อ module ควรเป็น lowercase** และใช้ underscore สำหรับคำหลายคำ
3. **ใช้ --dry-run** เพื่อดูไฟล์ที่จะสร้างก่อนสร้างจริง
4. **ใช้ --force** เมื่อต้องการเขียนทับไฟล์เดิม

## 🐛 Troubleshooting

### ปัญหาที่พบบ่อย

1. **Command not found: velo**

   ```bash
   # แก้ไข: ใช้ poetry run
   poetry run velo
   ```

2. **Module already exists**

   ```bash
   # แก้ไข: ใช้ --force flag
   poetry run velo module create products --force
   ```

3. **Permission denied**
   ```bash
   # แก้ไข: ตรวจสอบ file permissions
   chmod +x scripts/*
   ```

## 📚 เอกสารเพิ่มเติม

- [โครงสร้างโปรเจกต์](../README.md#📁-โครงสร้างโปรเจกต์)
- [Clean Architecture Guide](../.github/instructions/fastapi.instructions.md)
- [Development Best Practices](../README.md#📚-คู่มือการพัฒนา)
