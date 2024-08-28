from sqlalchemy.orm import mapped_column, Mapped
from app.model.base import Base


class BusinessUser(Base):
    __tablename__ = 'business_user'

    business_no: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    business_id: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    business_pwd: Mapped[str]
    business_name: Mapped[str]
    business_email: Mapped[str]
    address: Mapped[str]
    business_uploadno: Mapped[int]
