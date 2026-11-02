from sqlalchemy import String, Text, Integer, Boolean, BigInteger
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import TIMESTAMP
from db.database import Base

class TaskDB(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20))
    completed: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))
