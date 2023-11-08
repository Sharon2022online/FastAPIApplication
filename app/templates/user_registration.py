from fastapi import FastAPI, Body
from pydantic import BaseModel
from pymongo import MongoClient
import psycopg2
import hashlib
import os

def get_database_connection():
    # Get the password from an environment variable or secure storage
    password = os.environ.get('POSTGRES_PASSWORD')

    # Use the password to connect to the database
    connection = psycopg2.connect(
        host="localhost",
        database="registration",
        user="postgres",
        password=1234
    )
    return connection


app = FastAPI()

class User(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str

class ProfilePicture(BaseModel):
    profile_picture: str

# Connect to PostgreSQL database
connection = psycopg2.connect(
    host="localhost",
    database="registration",
    user="postgres",
    password="1234"
)

# Connect to MongoDB database
client = MongoClient("mongodb://localhost:27017/")
db = client["user_db"]
collection = db["profile_pictures"]

# Define a function to check if email already exists
def check_email_exists(email):
    cursor = connection.cursor()
    cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    return result is not None

# Define a function to register a new user
def register_user(user: User, profile_picture: ProfilePicture):
    # Check if email already exists
    if check_email_exists(user.email):
        raise ValueError("Email already exists")

    # Hash the password
    hashed_password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()

    # Save user details to PostgreSQL
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (full_name, email, password, phone) VALUES (%s, %s, %s, %s)",
                    (user.full_name, user.email, hashed_password, user.phone))
    connection.commit()
    cursor.close()

    # Save profile picture to MongoDB
    collection.insert_one({"email": user.email, "profile_picture": profile_picture.profile_picture})

# Define a function to get registered user details
def get_registered_user_details(email: str):
    # Retrieve user details from PostgreSQL
    cursor = connection.cursor()
    cursor.execute("SELECT full_name, phone FROM users WHERE email = %s", (email,))
    user_details = cursor.fetchone()
    cursor.close()

    if user_details is None:
        raise ValueError("User not found")

    # Retrieve profile picture from MongoDB
    profile_picture = collection.find_one({"email": email})["profile_picture"]

    return {
        "full_name": user_details[0],
        "phone": user_details[1],
        "profile_picture": profile_picture
    }

# Define endpoints for user registration and get user details
@app.post("/register")
def register_user_endpoint(user: User, profile_picture: ProfilePicture):
    register_user(user, profile_picture)
    return {"message": "User registered successfully"}

@app.get("/user/{email}")
def get_registered_user_details_endpoint(email: str):
    user_details = get_registered_user_details(email)
    return user_details
