from sqlalchemy.orm import Mapped, mapped_column

from bluestorage.databases.schema.base import Base 

class ItemInfo(Base):
    """
    FileInfo is class about file 
    """
    __tablename__ = "fileinfo"
    path: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column(default="None")

