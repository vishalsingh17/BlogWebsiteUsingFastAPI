from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from blog import schemas, models
from blog.database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Blog with id {id} not found")
    blog.update(request.dict())
    db.commit()
    return f"Blog with id {id} updated successfully"

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:int, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return f"Blog with id {id} deleted successfully!!"


@app.get('/blog', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def get_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_blog_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).where(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Blog with the {id} not found!!")
    return blog

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/user')
def create_user(request:schemas.User, db:Session = Depends(get_db)):
    hashedpwd = pwd_cxt.hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashedpwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
