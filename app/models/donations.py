from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
   from app.models.users import UserModel

class DonationModel(Base):
   __tablename__ = "donations"
   id: Mapped[int] = mapped_column(primary_key=True)
   project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
   user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
   amount: Mapped[int] = mapped_column(Integer, nullable=False)

   project: Mapped["ProjectModel"] = relationship("ProjectModel", foreign_keys=[project_id])
   user: Mapped["UserModel"] = relationship("UserModel", foreign_keys=[user_id])