from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent / ".env")

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL") or os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("Database URL is not set. Define SQLALCHEMY_DATABASE_URL or DATABASE_URL in the environment.")

# 2. Create the engine, it is responsible to connect sqlalchemy to postgres
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. Create the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4. The modern replacement for declarative_base()
class Base(DeclarativeBase):
    pass
