import datetime

from .. import schemas

from beanie import Document
from pydantic import Field


class User(schemas.User, Document):
    password: str
    roles: list[str] = ["user"]
    status: str = "active"

    register_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)

    class Settings:
        name = "users"

    async def has_roles(self, roles):
        for role in roles:
            if role in self.roles:
                return True
        return False

    async def set_password(self, password):
        from werkzeug.security import generate_password_hash

        self.password = generate_password_hash(password)

    async def verify_password(self, password):
        from werkzeug.security import check_password_hash

        if check_password_hash(self.password, password):
            return True
        return False

    async def is_use_citizen_id_as_password(self):
        from werkzeug.security import check_password_hash

        if check_password_hash(self.citizen_id, self.password):
            return True
        return False
