from fastapi import FastAPI
from routes.userRoute import userRouter
from routes.route import blogRouter
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

app = FastAPI()

app.include_router(userRouter, prefix="/users")
app.include_router(blogRouter, prefix="/blogs")
