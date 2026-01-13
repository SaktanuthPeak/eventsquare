"""
Base repository pattern implementation
"""

from typing import TypeVar, Generic, Optional, List, Dict, Any, Type, Union
from beanie import Document
from datetime import datetime
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import paginate
from pydantic import BaseModel


T = TypeVar("T", bound=Document)


class BaseRepository(Generic[T]):
    """Base repository with common CRUD operations"""

    def __init__(self, model: Type[T]):
        self.model = model

    async def create(self, entity: T) -> T:
        """Create a new entity"""
        return await entity.insert()

    async def find_by_id(
        self, entity_id: str, fetch_links: bool = False
    ) -> Optional[T]:
        """Find entity by ID"""
        try:
            return await self.model.get(entity_id, fetch_links=fetch_links)
        except Exception:
            return None

    async def find_one(
        self, filters: Dict[str, Any], fetch_links: bool = False
    ) -> Optional[T]:
        """Find one entity by filters"""
        return await self.model.find_one(filters, fetch_links=fetch_links)

    async def find_many(
        self,
        filters: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 100,
        fetch_links: bool = False,
        sort: Optional[List[tuple]] = None,
        as_list: bool = False,
    ) -> Union[Page[T], List[T]]:
        """Find multiple entities with filters (optional) using fastapi_pagination Beanie integration

        Args:
            filters: Optional filters to apply
            skip: Number of records to skip
            limit: Maximum number of records to return
            fetch_links: Whether to fetch linked documents
            sort: Optional sort criteria as list of tuples [(field, direction), ...]
            Example: [("created_at", -1), ("name", 1)]
            as_list: If True, returns List[T], if False returns Page[T] with pagination

        If filters is None, returns all entities
        """
        if filters:
            query = self.model.find(filters, fetch_links=fetch_links)
        else:
            query = self.model.find_all(fetch_links=fetch_links)

        if sort:
            query = query.sort(*sort)

        if as_list:
            return await query.skip(skip).limit(limit).to_list()
        else:
            return await paginate(query, fetch_links=fetch_links)

    async def update(self, entity_id: str, update_data: Dict[str, Any]) -> Optional[T]:
        """Update entity by ID"""
        entity = await self.find_by_id(entity_id)
        if not entity:
            return None

        # Add timestamp
        update_data["updated_at"] = datetime.utcnow()

        # Update fields
        for key, value in update_data.items():
            setattr(entity, key, value)

        await entity.save()
        return entity

    async def delete(self, entity_id: str) -> bool:
        """Delete entity by ID"""
        entity = await self.find_by_id(entity_id)
        if not entity:
            return False

        await entity.delete()
        return True

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count entities"""
        if filters:
            return await self.model.find(filters).count()
        return await self.model.find_all().count()

    async def exists(self, filters: Dict[str, Any]) -> bool:
        """Check if entity exists"""
        entity = await self.find_one(filters)
        return entity is not None

    def schema_dump(
        self, schema: BaseModel, exclude: Optional[List[str]] = None, **extra_fields
    ) -> T:
        """Create entity from Pydantic schema with extra fields"""
        exclude = exclude or []
        data = schema.model_dump(exclude=set(exclude))
        data.update(extra_fields)
        return self.model(**data)
