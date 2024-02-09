import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from bluestorage.databases.schema.base import Base 
from bluestorage.util import generate_token, get_expiration_date

class Token(Base):
    """
    Token is what need for access some resource
    """
    __tablename__ = "token"
    user_id: Mapped[str] = mapped_column(
        ForeignKey("user.id")
    )
    access_token: Mapped[str] = mapped_column(
        default_factory=generate_token
    )
    expiration_date: Mapped[datetime.datetime] = mapped_column(
        default_factory=get_expiration_date
    )

