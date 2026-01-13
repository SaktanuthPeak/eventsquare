"""
User repository for data access operations
"""

from typing import Optional
from beanie.operators import And, Or
from beanie.odm.operators.find.evaluation import RegEx
from ...core.base_repository import BaseRepository
from .model import User


class UserRepository(BaseRepository[User]):
    """Repository for User data operations - Data access only"""

    def __init__(self):
        super().__init__(User)

    async def find_by_username(self, username: str) -> Optional[User]:
        """Find user by username"""
        return await self.find_one({"username": username})

    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email"""
        return await self.find_one({"email": email})

    async def search_users(
        self,
        query: Optional[str] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
    ):
        """Search users with filters"""
        filters = self._build_search_filters(query, role, is_active)
        combined_filters = self._combine_filters(filters)
        
        return await self.find_many(
            filters=combined_filters,
            sort=[("created_at", -1)]
        )

    def _build_search_filters(
        self, 
        query: Optional[str], 
        role: Optional[str], 
        is_active: Optional[bool]
    ) -> list:
        """Build search filters based on parameters"""
        filters = []
        
        # Text search filter
        if query and query.strip():
            search_filter = Or(
                RegEx(User.username, query, options="i"),
                RegEx(User.email, query, options="i"),
                RegEx(User.name, query, options="i"),
            )
            filters.append(search_filter)

        # Role filter
        if role:
            filters.append(User.role == role)

        # Active status filter
        if is_active is not None:
            filters.append(User.is_active == is_active)

        return filters

    def _combine_filters(self, filters: list):
        """Combine multiple filters with AND operator"""
        if not filters:
            return {}
        
        return And(*filters) if len(filters) > 1 else filters[0]

    async def get_list(self): ...

    # สืบทอดจาก BaseRepository:
    # - find_by_id, find_many, update, delete ฯลฯ


# Dependency providers
async def get_user_repository() -> UserRepository:
    """Get user repository instance"""
    return UserRepository()
