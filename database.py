from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# We use SQLite for local development. In production, this string would point to PostgreSQL.
SQLALCHEMY_DATABASE_URL = "sqlite:///./springstreet.db"

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class to handle database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class that our database models will inherit from
Base = declarative_base()

# Dependency to get the database session in our API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()