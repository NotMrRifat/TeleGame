"""Generic Repository Pattern implementation for Async SQLAlchemy."""

import uuid
from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """Generic async repository providing standard CRUD operations."""

    def __init__(self, model_cls: type[T], session: AsyncSession):
        self.model_cls = model_cls
        self.session = session

    async def get_by_id(self, entity_id: uuid.UUID) -> T | None:
        """Fetch entity by UUID primary key."""
        stmt = select(self.model_cls).where(
            self.model_cls.id == entity_id,
            self.model_cls.is_deleted.is_(False),
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[T]:
        """Fetch all active non-deleted entities."""
        stmt = (
            select(self.model_cls)
            .where(self.model_cls.is_deleted.is_(False))
            .limit(limit)
            .offset(offset)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create(self, **kwargs: Any) -> T:
        """Create and persist a new entity."""
        instance = self.model_cls(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def update(self, entity_id: uuid.UUID, **kwargs: Any) -> T | None:
        """Update fields on an existing entity."""
        entity = await self.get_by_id(entity_id)
        if not entity:
            return None
        for key, value in kwargs.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        await self.session.flush()
        return entity

    async def soft_delete(self, entity_id: uuid.UUID) -> bool:
        """Soft delete an entity."""
        entity = await self.get_by_id(entity_id)
        if not entity:
            return False
        entity.is_deleted = True
        await self.session.flush()
        return True
