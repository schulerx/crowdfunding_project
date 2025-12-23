from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
if TYPE_CHECKING:
   from app.models.users import UserModel
   from app.models.categories import CategoriesModel



class ProjectModel(Base):
   __tablename__ = "projects"
   id: Mapped[int] = mapped_column(Integer, primary_key=True)
   creator_id: Mapped[int] = mapped_column(
       ForeignKey("users.id"),
       nullable=False
   )
   title: Mapped[str] = mapped_column(String(255), nullable=False)
   description: Mapped[str] = mapped_column(String(255), nullable=False)
   target_amount: Mapped[str] = mapped_column(String(65535), nullable=False)
   collected_amount: Mapped[str] = mapped_column(String(65535), nullable=False)
   category_id: Mapped[int] = mapped_column(
       ForeignKey("categories.id"),
       nullable=False
   )
   is_active: Mapped[bool] = mapped_column(Boolean, default=True)
   date_start: Mapped[int] = mapped_column(Integer, nullable=False)
   date_end: Mapped[int] = mapped_column(Integer, nullable=False)


   creator: Mapped["UserModel"] = relationship(
       "UserModel",
       foreign_keys=[creator_id]
   )
   category: Mapped["CategoriesModel"] = relationship(
       "CategoriesModel",
       foreign_keys=[category_id]
   )

