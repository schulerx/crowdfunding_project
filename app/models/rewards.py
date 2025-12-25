from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
if TYPE_CHECKING:

   from app.models.rewards import RewardModel
class RewardModel(Base):
   __tablename__ = "rewards"
   id: Mapped[int] = mapped_column(primary_key=True)

   title: Mapped[str] = mapped_column(String(255), nullable=True)
   description: Mapped[str] = mapped_column(String(255), nullable=True)
   required_quantity: Mapped[int] = mapped_column(Integer, nullable=True)
  