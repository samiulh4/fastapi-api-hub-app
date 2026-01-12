from pydantic import BaseModel
from typing import Optional, Literal

# Schema (Request) for creating a new blog post
class BlogCreate(BaseModel):
    blog_title: str
    blog_content: str
    #blog_author_id: str
    blog_img_id: Optional[str] = None # Feature image

# Schema (Response) for a blog post
class BlogResponse(BaseModel):
    id: str
    blog_title: str
    blog_content: str
    blog_author_id: str
    blog_img_id: Optional[str] = None # Feature image
    #created_at: datetime
    #blog_status: Literal["active", "inactive"]    

class AuthorResponse(BaseModel):
    id: str
    name: str
    email: str

class ImageResponse(BaseModel):
    id: str
    file_url: str


class BlogViewResponse(BaseModel):
    id: str
    blog_title: str
    blog_content: str
    author: AuthorResponse
    blog_img_id: Optional[str] = None    


