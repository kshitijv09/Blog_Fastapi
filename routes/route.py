from fastapi import Depends,APIRouter, HTTPException
from models.blogs import Blogs
from config.database import collection_name
from schema.schemas import individual_serial, list_serial
from bson import ObjectId
from jwt import verify_token, TokenData
blogRouter = APIRouter()

# Get all blogs
@blogRouter.get("/")
async def getBlogs(token_data: TokenData = Depends(verify_token)):
    blogs = list_serial(collection_name.find())
    return blogs

# Get blog by ID
@blogRouter.get("/{blog_id}")
async def getBlogById(blog_id: str):
    blog = collection_name.find_one({"_id": ObjectId(blog_id)})
    if blog:
        return individual_serial(blog)
    else:
        raise HTTPException(status_code=404, detail="Blog not found")

# Create a new blog
@blogRouter.post("/")
async def createBlog(blog: Blogs):
    new_blog = blog.dict()
      # Removing "id" field if present in the request
    inserted_blog = collection_name.insert_one(new_blog)
    return {"id": str(inserted_blog.inserted_id)}

# Update an existing blog
@blogRouter.put("/{blog_id}")
async def updateBlog(blog_id: str, blog: Blogs):
    updated_blog = blog.dict()
      # Removing "id" field if present in the request
    result = collection_name.update_one({"_id": ObjectId(blog_id)}, {"$set": updated_blog})
    if result.modified_count == 1:
        return {"message": "Blog updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Blog not found")

# Delete a blog
@blogRouter.delete("/{blog_id}")
async def deleteBlog(blog_id: str):
    result = collection_name.delete_one({"_id": ObjectId(blog_id)})
    if result.deleted_count == 1:
        return {"message": "Blog deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Blog not found")
