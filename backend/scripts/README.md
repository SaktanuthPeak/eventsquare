# Module Generator CLI

CLI script สำหรับสร้าง FastAPI modules ใหม่ตามโครงสร้าง Clean Architecture ของโปรเจค

## การใช้งาน

```bash
# รันจาก root directory ของโปรเจค
python scripts/create-module

# หรือ
./scripts/create-module
```

## วิธีการทำงาน

1. **ป้อนชื่อ feature**: ระบบจะถามชื่อ feature ที่ต้องการสร้าง

   - ใช้ lowercase เท่านั้น
   - สามารถใช้ underscore (\_) และตัวเลขได้
   - ตัวอย่าง: `products`, `user_profiles`, `order_items`

2. **ยืนยันการสร้าง**: กด `y` หรือ `yes` เพื่อยืนยัน

3. **ระบบจะสร้างไฟล์ทั้งหมด**:
   - `apiapp/modules/{feature}/`
     - `__init__.py`
     - `schemas.py` - Pydantic schemas (DTOs)
     - `repository.py` - Data access layer
     - `use_case.py` - Business logic layer
     - `router.py` - API endpoints
   - `apiapp/models/{feature}_model.py` - Beanie document model

## ตัวอย่างการใช้งาน

```bash
$ python scripts/create-module

🚀 FastAPI Module Generator
==================================================

📝 Enter feature name (e.g., 'products', 'orders', 'user_profiles'): products

📋 Creating module: products
📁 Location: apiapp/modules/products

❓ Create 'products' module? (y/N): y

🔨 Creating module structure...
📝 Creating __init__.py...
📝 Creating schemas.py...
📝 Creating repository.py...
📝 Creating use_case.py...
📝 Creating router.py...
📝 Creating model file...

✅ Successfully created 'products' module!
📁 Module path: /path/to/apiapp/modules/products
📄 Model file: /path/to/apiapp/models/products_model.py

🔧 Next steps:
1. Update apiapp/infrastructure/database.py to include Products model
2. Review and customize the generated files as needed
3. The router will be auto-discovered and included in the API

📝 Generated files:
   - /path/to/apiapp/modules/products/__init__.py
   - /path/to/apiapp/modules/products/schemas.py
   - /path/to/apiapp/modules/products/repository.py
   - /path/to/apiapp/modules/products/use_case.py
   - /path/to/apiapp/modules/products/router.py
   - /path/to/apiapp/models/products_model.py
```

## โครงสร้างที่สร้างขึ้น

### Schemas (DTOs)

- `{Feature}Base` - Base schema with common fields
- `{Feature}Request` - Request schema for creating/updating
- `{Feature}Response` - Response schema with additional fields

### Repository

- CRUD operations
- Custom query methods
- Inherits from `BaseRepository`

### Use Case

- Business logic
- Validation
- Dependency injection patterns
- Cross-module dependencies support

### Router

- REST API endpoints (GET, POST, PUT, DELETE)
- Authentication required
- Proper HTTP status codes
- Error handling

### Model

- Beanie document model
- MongoDB collection settings
- Indexes configuration

## หลังจากสร้าง Module

1. **อัพเดต database.py**:

   ```python
   # apiapp/infrastructure/database.py
   from ...models.{feature}_model import {Feature}

   # เพิ่มใน document_models list
   document_models = [
       User,
       {Feature},  # เพิ่มบรรทัดนี้
       # ... other models
   ]
   ```

2. **ปรับแต่งไฟล์ตามความต้องการ**:

   - แก้ไข fields ใน schemas
   - เพิ่ม business logic ใน use case
   - เพิ่ม custom query methods ใน repository
   - ปรับแต่ง API endpoints ใน router

3. **Router จะถูก auto-discover โดยอัตโนมัติ**

## ข้อกำหนด

- รันจาก root directory ของโปรเจค
- Python 3.8+
- โปรเจคต้องมี `apiapp` directory

## Error Handling

- ตรวจสอบชื่อ feature ที่ถูกต้อง
- ป้องกันการสร้าง module ซ้ำ
- ตรวจสอบ directory structure
- แสดง error message ที่ชัดเจน
