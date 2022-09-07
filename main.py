from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def index(limit = 10, published:bool = True, sort:Optional[str] = None):
    if published:
        return f"{limit} published blogs from the database"
    return f"{limit} blogs from the database"

@app.get('/unpublsihed')
def unpublished():
    return {"data": "unpublished"}

@app.get('/blog/{id}')
def show(id :  int):
    return {"data": id}

@app.get('/blog/{id}/comments')
def get_comments(id):
    return {"data": {"1", "2"}}

class CreateBlog(BaseModel):
    title:str
    body: str
    published: Optional[bool]

@app.post('/create_blog')
def create_blog(blog_create:CreateBlog):
    return f"Blog title is '{blog_create.title}' and body is '{blog_create.body}'"