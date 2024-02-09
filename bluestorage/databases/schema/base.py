from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    MappedAsDataclass,
    DeclarativeBase,
    Mapped,
    mapped_column
)

class Base(MappedAsDataclass, DeclarativeBase, AsyncAttrs):
    id: Mapped[str] = mapped_column(
        default=None, 
        kw_only=True, 
        primary_key=True, 
        unique=True, 
        nullable=False
    )


