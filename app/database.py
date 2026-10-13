from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Use SQLite for development. For PostgreSQL, change to: "postgresql://user:pass@host/db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost/fastapi"

# 'check_same_thread' is required only for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# Each instance of SessionLocal will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for database models to inherit from
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()