try:
    from .database import Base
except ImportError:
    from database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, text

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=text('TRUE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'), nullable=False)


class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'), nullable=False)