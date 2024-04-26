from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List

# Initialize FastAPI app
app = FastAPI()

# Initialize MongoDB client
client = MongoClient('mongodb+srv://todo:ZwRWBHBaZApUmv1u@cluster0.9lerpi7.mongodb.net/')
db = client.todo_db
collection = db.todos

# Secret key for token
SECRET_KEY = "security-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Token security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User model for registration
class User(BaseModel):
    username: str
    password: str

# User model for authentication
class UserInDB(BaseModel):
    username: str
    hashed_password: str

# Todo model
class Todo(BaseModel):
    title: str
    description: str
    done: bool = False # Default value

# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to get user by username
def get_user(username: str):
    user_data = db.users.find_one({"username": username})
    if user_data:
        return UserInDB(**user_data)

# Function to authenticate user
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Function to create session
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.post("/register")
def register_user(user: User):
    hashed_password = pwd_context.hash(user.password)
    user_data = {"username": user.username, "hashed_password": hashed_password}
    db.users.insert_one(user_data)
    return {"message": "User registered successfully"}

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/todos/", response_model=List[Todo])
def read_todos(token: str = Depends(oauth2_scheme)):
    # Token verification can be added here
    todos = collection.find()
    return list(todos)

@app.post("/todos/")
def create_todo(todo: Todo, token: str = Depends(oauth2_scheme)):
    # Token verification can be added here
    todo_id = collection.insert_one(todo.dict()).inserted_id
    return {"message": "Todo created successfully", "todo_id": str(todo_id)}

@app.get("/todos/{todo_title}", response_model=Todo)
def read_todo(todo_title: str, token: str = Depends(oauth2_scheme)):
    # Token verification can be added here
    todo = collection.find_one({"title": todo_title})
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_title}")
def update_todo(todo_title: str, todo: Todo, token: str = Depends(oauth2_scheme)):
    # Token verification can be added here
    updated_todo = collection.update_one({"title": todo_title}, {"$set": todo.dict()})
    if updated_todo.modified_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo updated successfully"}

@app.delete("/todos/{todo_title}")
def delete_todo(todo_title: str, token: str = Depends(oauth2_scheme)):
    # Token verification can be added here
    deleted_todo = collection.delete_one({"title": todo_title})
    if deleted_todo.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}
