from sqlalchemy.orm import Mapped, mapped_column

from bluestorage.databases.schema.base import Base 

class User(Base):
    """
    FileInfo is class about file 
    """
    __tablename__ = "user"
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()

