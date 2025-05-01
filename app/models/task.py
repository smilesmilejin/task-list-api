from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from sqlalchemy import DateTime
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Wave 1
    title:Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
