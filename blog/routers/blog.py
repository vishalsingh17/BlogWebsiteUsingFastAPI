from typing import List
from fastapi import APIRouter, status, Depends, Session
from blog import schemas, database, models

router = APIRouter()

@router.get('/blog', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog], tags=['Blogs'])
def get_blog(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

