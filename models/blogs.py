from pydantic import BaseModel

class Blogs(BaseModel):
    title:str
    tag:str
    content:str
    date:str
    author:str
