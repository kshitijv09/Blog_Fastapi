from fastapi import FastAPI
from app.routes.userRoute import userRouter
from app.routes.blogRoute import blogRouter
from dotenv import load_dotenv



load_dotenv()

app = FastAPI()

app.include_router(userRouter, prefix="/user")
app.include_router(blogRouter, prefix="/blog")
