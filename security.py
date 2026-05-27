from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI
from dotenv import load_dotenv
import os 

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES"))

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

bcrypt_content = CryptContext(schemes=["argon2"], deprecated="auto")