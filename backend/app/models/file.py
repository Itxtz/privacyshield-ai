from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from app.db.base import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)

    filename = Column(String)

    filepath = Column(String)

    uploaded_by = Column(
    Integer,
    ForeignKey("users.id")
    )

    upload_time = Column(
        DateTime,
        default=datetime.utcnow
    )