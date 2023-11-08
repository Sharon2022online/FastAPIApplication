from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from . import database  # Import your database setup
from .models import User
from .schemas import UserRegistration

router = APIRouter()

# Define a route for user registration
@router.post("/register", response_model=UserRegistration)
def register_user(
    user_data: UserRegistration, profile_picture: UploadFile = File(...), db: Session = Depends(database.get_db)
):
    # Your user registration logic here, similar to what you have in main.py
    # Ensure you validate the user data and save it to your PostgreSQL and MongoDB databases

    return user_data

