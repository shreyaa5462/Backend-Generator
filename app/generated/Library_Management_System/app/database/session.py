import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Retrieve the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

# Create a reusable SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

# Configure a session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for declarative models
Base = declarative_base()

def get_db():
    """FastAPI dependency that provides a database session.
    Usage:
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create all tables defined by declarative models.
    Call this at application startup if you need automatic table creation.
    """
    Base.metadata.create_all(bind=engine)