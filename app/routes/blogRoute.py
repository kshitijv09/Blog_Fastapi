from fastapi import Depends, APIRouter, HTTPException, Query, status
from app.models.blogs import Blogs
from config.blogdatabase import collection_name
from app.schema.schemas import individual_serial, list_serial
from bson import ObjectId
from jwt import verify_token, TokenData
from app.routes.userRoute import get_user_by_id

blogRouter = APIRouter()

@blogRouter.get("/")
async def get_blogs(token_data: TokenData = Depends(verify_token)):
    blogs = list_serial(collection_name.find())
    return blogs

@blogRouter.get("/{blog_id}")
async def get_blog_by_id(blog_id: str,token_data: TokenData =Depends(verify_token)):
    blog = collection_name.find_one({"_id": ObjectId(blog_id)})
    if blog:
        return individual_serial(blog)
    else:
        raise HTTPException(status_code=404, detail="Blog not found")

@blogRouter.get("/{user_id}/blogs")
async def get_blog_by_user(user_id: str, limit: int = Query(10, description="Number of blogs to return per page"), skip: int = Query(0, description="Number of blogs to skip"),token_data: TokenData =Depends(verify_token)):
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_interests = [interest["name"] for interest in user.get("interests", [])]

    blogs = list_serial(collection_name.find())
    blogs.sort(key=lambda x: user_interests.index(x["tag"]) if x["tag"] in user_interests else len(user_interests))

    paginated_blogs = blogs[skip: skip + limit]
    return paginated_blogs

@blogRouter.post("/")
async def create_blog(blog: Blogs,token_data: TokenData =Depends(verify_token)):
    if not blog:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request. Blog data is missing.")

    new_blog = blog.dict()

    try:
        inserted_blog = collection_name.insert_one(new_blog)
        return {"id": str(inserted_blog.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")

@blogRouter.put("/{blog_id}")
async def update_blog(blog_id: str, blog: Blogs,token_data: TokenData =Depends(verify_token)):
    updated_blog = blog.dict()
    result = collection_name.update_one({"_id": ObjectId(blog_id)}, {"$set": updated_blog})
    if result.modified_count == 1:
        return {"message": "Blog updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Blog not found")

@blogRouter.delete("/{blog_id}")
async def delete_blog(blog_id: str,token_data: TokenData =Depends(verify_token)):
    result = collection_name.delete_one({"_id": ObjectId(blog_id)})
    if result.deleted_count == 1:
        return {"message": "Blog deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Blog not found")
