"""
Base use case pattern implementation
"""

from typing import TypeVar, Optional, Dict, Any, Generic, Union, Type
from abc import ABC
from beanie import Document
from fastapi_pagination import Page
from pydantic import BaseModel

from .base_repository import BaseRepository
from .exceptions import BusinessLogicError


T = TypeVar("T", bound=Document)
R = TypeVar("R", bound=BaseRepository)
S = TypeVar("S", bound=BaseModel)  # Schema type


class BaseUseCase(ABC, Generic[T, R, S]):
    """Simple base use case for business logic"""

    def __init__(self, repository: R, response_schema: Type[S]):
        self.repository = repository
        self.response_schema = response_schema

    # CRUD Operations
    async def create(self, data: Union[BaseModel, Dict[str, Any]]) -> S:
        """Create a new entity and return as response schema"""
        try:
            # Convert schema to dict if needed
            create_data = data.model_dump() if isinstance(data, BaseModel) else data
            entity = await self.repository.create(create_data)
            return self.convert_to_response_schema(entity, self.response_schema)
        except Exception as e:
            raise BusinessLogicError(f"Creation failed: {str(e)}")

    async def get_by_id(self, entity_id: str, **kwargs) -> Optional[S]:
        """Get entity by ID and return as response schema

        Args:
            entity_id: The ID of the entity to retrieve
            **kwargs: Additional parameters to pass to the repository (e.g., fetch_links=True)
        """
        entity = await self.repository.find_by_id(entity_id, **kwargs)
        return self.convert_to_response_schema(entity, self.response_schema)

    async def get_list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 100,
        **kwargs,
    ) -> Page[S]:
        """Get all entities with pagination using Beanie's integration with fastapi_pagination
        Always returns Page[ResponseSchema] instead of Page[Document]

        Args:
            filters: Optional filters to apply
            skip: Number of records to skip
            limit: Maximum number of records to return
            **kwargs: Additional parameters to pass to the repository (e.g., fetch_links=True)
        """
        # Get paginated documents from repository
        documents_page = await self.repository.find_many(filters, skip, limit, **kwargs)

        # Convert to response schema page
        return self.convert_page_to_response_schema(
            documents_page, self.response_schema
        )

    async def update(
        self, entity_id: str, data: Union[BaseModel, Dict[str, Any]]
    ) -> Optional[S]:
        """Update entity and return as response schema"""
        existing = await self.repository.find_by_id(entity_id)
        if not existing:
            return None

        try:
            # Convert schema to dict if needed
            update_data = data.model_dump() if isinstance(data, BaseModel) else data
            updated = await self.repository.update(entity_id, update_data)
            return self.convert_to_response_schema(updated, self.response_schema)
        except Exception as e:
            raise BusinessLogicError(f"Update failed: {str(e)}")

    async def delete(self, entity_id: str) -> bool:
        """Delete entity"""
        existing = await self.repository.find_by_id(entity_id)
        if not existing:
            return False

        try:
            success = await self.repository.delete(entity_id)
            return success
        except Exception as e:
            raise BusinessLogicError(f"Deletion failed: {str(e)}")

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count entities"""
        return await self.repository.count(filters)

    async def exists(self, filters: Dict[str, Any]) -> bool:
        """Check if entity exists"""
        return await self.repository.exists(filters)

    # Utility methods
    def convert_to_response_schema(
        self, model: Optional[T], schema_class: Type[S]
    ) -> Optional[S]:
        """Convert model to response schema"""
        if model is None:
            return None
        return schema_class.model_validate(model.model_dump())

    def convert_page_to_response_schema(
        self, page: Page[T], schema_class: Type[S]
    ) -> Page[S]:
        """Convert Page[Model] to Page[ResponseSchema]"""
        response_items = [
            schema_class.model_validate(item.model_dump()) for item in page.items
        ]

        return Page(
            items=response_items,
            total=page.total,
            page=page.page,
            size=page.size,
            pages=page.pages,
        )
