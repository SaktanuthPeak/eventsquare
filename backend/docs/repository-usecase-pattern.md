# 📚 Repository และ Use Case Pattern

## 🎯 ภาพรวม

Repository และ Use Case Pattern เป็นส่วนสำคัญของ Clean Architecture ที่ช่วยแยกชั้นงานให้ชัดเจน ทำให้โค้ดง่ายต่อการทดสอบ บำรุงรักษา และขยาย

## 🏗️ โครงสร้างของ Pattern

```
modules/{feature}/
├── repository.py   # Data Access Layer - จัดการการเข้าถึงข้อมูล
├── use_case.py     # Business Logic Layer - ประมวลผลตามกฎธุรกิจ
└── router.py       # Presentation Layer - รับ/ส่งข้อมูลผ่าน API
```

## 📊 Repository Pattern

### 🎯 หน้าที่ของ Repository

Repository เป็นชั้นที่รับผิดชอบการเข้าถึงข้อมูล (Data Access Layer) โดย:

- **แยก Business Logic ออกจาก Data Logic**
- **สร้าง Interface ที่เป็นมิตรสำหรับ Business Layer**
- **ซ่อนรายละเอียดของ Database Implementation**
- **ทำให้ง่ายต่อการ Mock ในการทดสอบ**

### 🔧 BaseRepository

โปรเจกต์นี้มี `BaseRepository` ที่มีฟังก์ชัน CRUD พื้นฐาน:

```python
from apiapp.core.base_repository import BaseRepository
from typing import Optional, Dict, Any, List
from fastapi_pagination import Page
from beanie.operators import And, Or

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)
    
    # สืบทอดฟังก์ชันพื้นฐานจาก BaseRepository:
    # - create(entity)
    # - find_by_id(id, fetch_links=False)
    # - find_one(filters, fetch_links=False)
    # - find_many(filters, skip, limit, fetch_links, sort, as_list)
    # - update(id, data)
    # - delete(id)
    
    # เพิ่มฟังก์ชันเฉพาะ Business
    async def find_by_email(self, email: str) -> Optional[User]:
        """หาผู้ใช้จาก email"""
        return await self.find_one({"email": email})
    
    async def find_active_users(self) -> Page[User]:
        """หาผู้ใช้ที่ active เท่านั้น"""
        return await self.find_many(
            User.is_active == True,  # Beanie operators (แนะนำ)
            sort=[("created_at", -1)]
        )
    
    async def search_users(self, query: str) -> Page[User]:
        """ค้นหาผู้ใช้จากชื่อหรือ email"""
        return await self.find_many(
            Or(
                User.full_name.regex(query, "i"),
                User.email.regex(query, "i")
            )
        )
```

### 🔍 Query Patterns

#### 1. PyMongo Style (ใช้ได้แต่ไม่แนะนำ)

```python
# ❌ PyMongo style - ไม่มี type safety
users = await repository.find_many({
    "age": {"$gt": 18},
    "status": "active"
})
```

#### 2. Beanie Operators (แนะนำ) ⭐

```python
# ✅ Beanie operators - มี type safety และอ่านง่าย
from beanie.operators import And, Or, In, Regex

# การกรองแบบง่าย
adults = await repository.find_many(User.age > 18)

# การกรองแบบซับซ้อน
active_adults = await repository.find_many(
    And(User.age >= 18, User.status == "active")
)

# การค้นหาด้วย regex
users = await repository.find_many(
    User.name.regex("john", "i")  # case-insensitive
)

# การกรองหลายค่า
vip_users = await repository.find_many(
    User.role.in_(["admin", "premium"])
)

# การรวมเงื่อนไข
result = await repository.find_many(
    Or(
        And(User.role == "admin", User.is_active == True),
        And(User.role == "premium", User.credits > 100)
    )
)
```

### 📄 Pagination และ Sorting

```python
# Pagination แบบเต็ม (ส่งคืน Page object)
users_page = await repository.find_many(
    filters=User.is_active == True,
    skip=0,
    limit=20,
    sort=[("created_at", -1), ("name", 1)],
    fetch_links=True
)
# Return: Page[User] พร้อม metadata

# List แบบธรรมดา (ส่งคืน List เฉยๆ)
users_list = await repository.find_many(
    filters=User.is_active == True,
    limit=100,
    as_list=True
)
# Return: List[User]
```

## 💼 Use Case Pattern

### 🎯 หน้าที่ของ Use Case

Use Case เป็นชั้นที่รับผิดชอบ Business Logic โดย:

- **ประมวลผลตามกฎธุรกิจ**
- **ควบคุม Transaction และ Data Consistency**
- **จัดการ Error Handling**
- **ทำหน้าที่เป็นตัวกลางระหว่าง Router และ Repository**

### 🔧 BaseUseCase

```python
from apiapp.core.base_use_case import BaseUseCase
from apiapp.core.exceptions import BusinessLogicError
from typing import Optional, Dict, Any
from fastapi_pagination import Page

class UserUseCase(BaseUseCase[User, UserRepository]):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)
    
    # สืบทอดฟังก์ชันพื้นฐานจาก BaseUseCase:
    # - create(data)
    # - get_by_id(id, **kwargs)
    # - get_all(filters, skip, limit, **kwargs)
    # - update(id, data)
    # - delete(id)
    
    async def register_user(self, user_data: Dict[str, Any]) -> User:
        """สมัครสมาชิกใหม่ พร้อม business logic"""
        
        # ตรวจสอบว่า email ซ้ำหรือไม่
        existing_user = await self.repository.find_by_email(user_data["email"])
        if existing_user:
            raise BusinessLogicError("Email already registered")
        
        # เข้ารหัสรหัสผ่าน
        user_data["password"] = hash_password(user_data["password"])
        
        # ตั้งค่าเริ่มต้น
        user_data["is_active"] = True
        user_data["role"] = "user"
        user_data["created_at"] = datetime.utcnow()
        
        # บันทึกข้อมูล
        return await self.create(user_data)
    
    async def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        """เปลี่ยนรหัสผ่าน พร้อมตรวจสอบรหัสเก่า"""
        
        user = await self.get_by_id(user_id)
        if not user:
            raise BusinessLogicError("User not found")
        
        # ตรวจสอบรหัสผ่านเก่า
        if not verify_password(old_password, user.password):
            raise BusinessLogicError("Invalid old password")
        
        # เปลี่ยนรหัสผ่านใหม่
        hashed_password = hash_password(new_password)
        await self.update(user_id, {"password": hashed_password})
        
        return True
    
    async def get_user_profile(self, user_id: str) -> Optional[User]:
        """ดูโปรไฟล์ผู้ใช้ พร้อม linked documents"""
        return await self.get_by_id(user_id, fetch_links=True)
    
    async def search_users(self, query: str, page: int = 1, size: int = 20) -> Page[User]:
        """ค้นหาผู้ใช้ตามคำค้น"""
        if len(query.strip()) < 2:
            raise BusinessLogicError("Search query must be at least 2 characters")
        
        skip = (page - 1) * size
        return await self.repository.search_users(query)
```

## 🔗 การใช้งานใน Router

```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserRegisterRequest,
    user_use_case: UserUseCase = Depends(get_user_use_case)
):
    """สมัครสมาชิกใหม่"""
    try:
        user = await user_use_case.register_user(user_data.model_dump())
        return user
    except BusinessLogicError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/search", response_model=Page[UserResponse])
async def search_users(
    q: str,
    page: int = 1,
    size: int = 20,
    user_use_case: UserUseCase = Depends(get_user_use_case)
):
    """ค้นหาผู้ใช้"""
    try:
        return await user_use_case.search_users(q, page, size)
    except BusinessLogicError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    user_use_case: UserUseCase = Depends(get_user_use_case)
):
    """ดูโปรไฟล์ตัวเอง"""
    return await user_use_case.get_user_profile(current_user.id)
```

## 🎯 หลักการสำคัญ

### ✅ DO - สิ่งที่ควรทำ

1. **Repository เข้าถึงข้อมูลเท่านั้น**
   ```python
   # ✅ ถูกต้อง
   async def find_active_users(self) -> Page[User]:
       return await self.find_many(User.is_active == True)
   ```

2. **Use Case ใส่ Business Logic**
   ```python
   # ✅ ถูกต้อง
   async def deactivate_user(self, user_id: str) -> bool:
       user = await self.get_by_id(user_id)
       if user.role == "admin":
           raise BusinessLogicError("Cannot deactivate admin user")
       return await self.update(user_id, {"is_active": False})
   ```

3. **ใช้ Beanie Operators สำหรับ Type Safety**
   ```python
   # ✅ ถูกต้อง
   return await self.find_many(
       And(User.age >= 18, User.status == "active")
   )
   ```

4. **ส่งผ่าน Parameters ด้วย kwargs**
   ```python
   # ✅ ถูกต้อง
   user = await user_use_case.get_by_id(user_id, fetch_links=True)
   ```

### ❌ DON'T - สิ่งที่ไม่ควรทำ

1. **ไม่ใส่ Business Logic ใน Repository**
   ```python
   # ❌ ผิด
   async def register_user(self, user_data: Dict) -> User:
       if user_data["age"] < 18:  # Business logic ใน Repository
           raise ValueError("User must be 18+")
       return await self.create(user_data)
   ```

2. **ไม่เข้าถึง Model โดยตรงใน Router**
   ```python
   # ❌ ผิด
   @router.get("/users")
   async def get_users():
       return await User.find_all().to_list()  # ข้าม Repository และ Use Case
   ```

3. **ไม่ใช้ Raw MongoDB Queries โดยไม่จำเป็น**
   ```python
   # ❌ ผิด - ไม่มี type safety
   users = await self.find_many({"age": {"$gte": 18}})
   
   # ✅ ถูกต้อง - มี type safety
   users = await self.find_many(User.age >= 18)
   ```

## 🧪 การทดสอบ

### Repository Testing

```python
import pytest
from unittest.mock import AsyncMock
from apiapp.modules.user.repository import UserRepository

@pytest.fixture
async def user_repository():
    return UserRepository()

async def test_find_by_email(user_repository):
    # Mock การค้นหา
    user_repository.find_one = AsyncMock(return_value=mock_user)
    
    result = await user_repository.find_by_email("test@example.com")
    
    assert result == mock_user
    user_repository.find_one.assert_called_once_with({"email": "test@example.com"})
```

### Use Case Testing

```python
import pytest
from unittest.mock import AsyncMock
from apiapp.modules.user.use_case import UserUseCase
from apiapp.core.exceptions import BusinessLogicError

@pytest.fixture
def user_use_case():
    mock_repo = AsyncMock()
    return UserUseCase(mock_repo)

async def test_register_user_duplicate_email(user_use_case):
    # Setup mock
    user_use_case.repository.find_by_email.return_value = mock_existing_user
    
    # Test
    with pytest.raises(BusinessLogicError, match="Email already registered"):
        await user_use_case.register_user({"email": "test@example.com"})
```

## 📊 ตัวอย่างการใช้งานจริง

### E-commerce Product Module

```python
# repository.py
class ProductRepository(BaseRepository[Product]):
    async def find_by_category(self, category: str) -> Page[Product]:
        return await self.find_many(
            Product.category == category,
            sort=[("created_at", -1)]
        )
    
    async def find_in_price_range(self, min_price: float, max_price: float) -> Page[Product]:
        return await self.find_many(
            And(Product.price >= min_price, Product.price <= max_price)
        )

# use_case.py
class ProductUseCase(BaseUseCase[Product, ProductRepository]):
    async def create_product(self, product_data: Dict[str, Any]) -> Product:
        # Business validation
        if product_data["price"] <= 0:
            raise BusinessLogicError("Price must be positive")
        
        # Auto-generate SKU
        product_data["sku"] = generate_sku(product_data["name"])
        product_data["created_at"] = datetime.utcnow()
        
        return await self.create(product_data)
    
    async def apply_discount(self, product_id: str, discount_percent: float) -> Product:
        if discount_percent < 0 or discount_percent > 50:
            raise BusinessLogicError("Discount must be between 0-50%")
        
        product = await self.get_by_id(product_id)
        if not product:
            raise BusinessLogicError("Product not found")
        
        new_price = product.price * (1 - discount_percent / 100)
        return await self.update(product_id, {"price": new_price})
```

## 🔧 การปรับแต่งขั้นสูง

### Custom Repository Methods

```python
class OrderRepository(BaseRepository[Order]):
    async def find_by_status_and_date(
        self, 
        status: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> Page[Order]:
        return await self.find_many(
            And(
                Order.status == status,
                Order.created_at >= start_date,
                Order.created_at <= end_date
            ),
            sort=[("created_at", -1)]
        )
    
    async def get_revenue_summary(self, start_date: datetime, end_date: datetime) -> Dict:
        # ใช้ MongoDB aggregation สำหรับการคำนวณที่ซับซ้อน
        pipeline = [
            {"$match": {
                "status": "completed",
                "created_at": {"$gte": start_date, "$lte": end_date}
            }},
            {"$group": {
                "_id": None,
                "total_revenue": {"$sum": "$total_amount"},
                "order_count": {"$sum": 1},
                "avg_order_value": {"$avg": "$total_amount"}
            }}
        ]
        
        result = await self.model.aggregate(pipeline).to_list()
        return result[0] if result else {"total_revenue": 0, "order_count": 0, "avg_order_value": 0}
```

## 🚀 สรุป

Repository และ Use Case Pattern ช่วยให้:

- **โค้ดแยกชั้นชัดเจน** - แต่ละชั้นมีหน้าที่เฉพาะ
- **ง่ายต่อการทดสอบ** - Mock ได้ง่าย
- **ใช้ซ้ำได้** - Business Logic แยกออกจาก Data Access
- **ปรับปรุงได้ง่าย** - เปลี่ยน Database หรือ Business Rule ได้โดยไม่กระทบส่วนอื่น
- **Type Safety** - ใช้ Beanie Operators เพื่อความปลอดภัย

การเรียนรู้ Pattern เหล่านี้จะทำให้คุณเขียน FastAPI ได้อย่างมืออาชีพและมีโครงสร้างที่ดี! 🎯