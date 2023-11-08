from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

# FastAPI instance
app = FastAPI()

# Create a template renderer
templates = Jinja2Templates(directory="templates")

# PostgreSQL Database Connection
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/REGISTRATION"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB Database Connection
MONGODB_URL = "mongodb://localhost:27017/"
client = MongoClient(MONGODB_URL)
db = client["registration"]

# Define your HTML template route for the login page
@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Define the user registration route
class UserRegistration(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str

# Placeholder for generating a unique user ID
def generate_user_id():
    return "some_unique_id"  # Implement your own logic here

@app.post("/register")
async def register_user(user_data: UserRegistration, profile_picture: UploadFile):
    try:
        # Validate user data (Pydantic will handle validation)

        # Storing Data in PostgreSQL
        from .models import User  # Import your User model
        user_model = User(full_name=user_data.full_name, email=user_data.email, password=user_data.password, phone=user_data.phone)
        db_pg = SessionLocal()
        db_pg.add(user_model)
        db_pg.commit()
        db_pg.close()

        # Storing Profile Picture in MongoDB
        user_id = generate_user_id()  # Implement your own logic to generate a unique user ID
        db_mongo = client["registration"]
        db_mongo["profile_pictures"].insert_one({"_id": user_id, "profile_picture": profile_picture.file.read()})

        # Return a success response
        return {"message": "Registration successful"}

    except Exception as e:
        # Log the error for debugging
        print(f"Registration error: {str(e)}")
        # Return an error response
        return {"message": "Registration failed"}
