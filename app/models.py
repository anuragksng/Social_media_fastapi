try:
    from .database import Base
except ImportError:
    from database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, text, ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=text('TRUE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'), nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User") #creates an ORM-level link from a Post row to the corresponding User row. Tells SQLAlchemy: when I access post.owner, load the matching User object for the owner_id value.

class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'), nullable=False)