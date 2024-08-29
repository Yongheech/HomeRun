from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from app.model.base import Base


class User(Base):
    __tablename__ = 'user'

    userno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    userid: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    passwd: Mapped[str]
    name: Mapped[str]
    email: Mapped[str]
    phone: Mapped [str]
    birth: Mapped[str] = mapped_column(String)
    regisdate: Mapped[datetime] = mapped_column(default=datetime.now)
    modifydate: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)




