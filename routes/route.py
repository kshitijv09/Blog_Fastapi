from fastapi import Depends,APIRouter, HTTPException, Query,status
from models.blogs import Blogs
from config.database import collection_name
from schema.schemas import individual_serial, list_serial
from bson import ObjectId
from jwt import verify_token, TokenData
from bson import ObjectId
from routes.userRoute  import get_user_by_id
blogRouter = APIRouter()

# Get all blogs
@blogRouter.get("/")
async def getBlogs(token_data: TokenData = Depends(verify_token)):
    print(token_data)
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

@blogRouter.get("/{user_id}/blogs")
async def getBlogByUser(user_id: str, limit: int = Query(10, description="Number of blogs to return per page"),skip: int = Query(0, description="Number of blogs to skip")):
    user=get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_interests = user.get("interests", [])

    user_interests = [interest["name"] for interest in user_interests]
    print("User interest",user_interests)
    """ blogs = collection_name.find({"tag": {"$in": user_interests}}) """
    blogs=list_serial(collection_name.find())
    print("Blogs are ",blogs)
    
    # Sort blogs based on the user's interests
    blogs.sort(key=lambda x: user_interests.index(x["tag"]) if x["tag"] in user_interests else len(user_interests))
# Sort blogs based on the user's interests
    print("SBlogs are ",blogs)
    """ for blog in sorted_blogs:
        blog.pop('_id', None) """
    paginated_blogs = blogs[skip:skip + limit]
    return paginated_blogs

# Create a new blog
@blogRouter.post("/")
async def createBlog(blog: Blogs):
    if not blog:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request. Blog data is missing.")
    
    new_blog = blog.dict()

    try:
        inserted_blog = collection_name.insert_one(new_blog)
        return {"id": str(inserted_blog.inserted_id)}
    except Exception as e:
        # Handle other types of errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")

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
