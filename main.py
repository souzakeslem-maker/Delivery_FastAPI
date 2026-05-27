from fastapi import FastAPI
#from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os 


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACESS_TOKEN_EXPIRE_MINUTES")

app = FastAPI()

# oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")



from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

