from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class UserDB(Base):
    # TODO: Define the UserDB model with appropriate fields and relationships
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, index=True)
    age: Mapped[int] = mapped_column(Integer)
    accounts: Mapped[list["AccountDB"]] = relationship("AccountDB", back_populates="user", cascade="all, delete-orphan")

class AccountDB(Base):
    # TODO: Define the AccountDB model with appropriate fields and relationships
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    account_number: Mapped[str] = mapped_column(String, index=True)
    account_type: Mapped[str] = mapped_column(String, index=True)
    balance: Mapped[float] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["UserDB"] = relationship("UserDB", back_populates="accounts")