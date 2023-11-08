 from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

# SQLAlchemy - PostgreSQL Database Connection
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/REGISTRATION"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB Database Connection
MONGODB_URL = "mongodb://localhost:27017/"
client = MongoClient(MONGODB_URL)
db = client["registration"]

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(String)
    profile_picture = Column(LargeBinary)

Base.metadata.create_all(bind=engine)

