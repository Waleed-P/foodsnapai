from sqlalchemy import Integer, String, Float, Enum
from app.enum.job_status import JobStatus
from datetime import datetime
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.model.user import UserModel

class FoodItemModel(Base):
    __tablename__ = "food_items"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Nullable/Optional fields (use Optional[] or | None)
    name: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    calories: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    protein: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    carbohydrates: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    fats: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Non-nullable fields
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    aws_unique_name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(Enum(JobStatus),default=JobStatus.PENDING, nullable=False)
    
    # Date and Foreign Key fields
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Relationship type hinting
    owner: Mapped["UserModel"] = relationship("UserModel", back_populates="food_items")