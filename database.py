from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry

# Define a registry
mapper_registry = registry()

"""
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
"""
SQLALCHEMY_DATABASE_URL = ("postgresql://dgvlrrpa:Zkew136ffOTwBF00i_gTzfAwvI-uPowH@rosie"
                           ".db.elephantsql.com/dgvlrrpa")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
Base = mapper_registry.generate_base()
