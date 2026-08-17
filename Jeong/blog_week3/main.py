from fastapi import FastAPI, status, HTTPException
from schema.request import BlogRequest, BlogUpdateRequest
from schema.response import BlogResponse
from database.db_connection import SessionFactory, engine
from database.orm import Base   
from model import Blog
from sqlalchemy import select, update, delete

Base.metadata.create_all(bind=engine)
app = FastAPI()

# blogs=[{"id": 1, "title": "First Blog", "content": "This is the first blog content."},
#        {"id": 2, "title": "Second Blog", "content": "This is the second blog content."},
#        {"id": 3, "title": "Third Blog", "content": "This is the third blog content."}]

@app.get("/blog", response_model=list[BlogResponse], status_code=status.HTTP_200_OK)
def get_blog():
    session = SessionFactory()
    try:
        stmt = select(Blog)
        blogs = session.execute(stmt).scalars().all()
        return blogs
    finally:
        session.close()

@app.get("/blog/{id}", response_model=BlogResponse, status_code=status.HTTP_200_OK)
def get_blog_id(id: int):
    session = SessionFactory()
    try:
        stmt = select(Blog).where(Blog.id == id)
        blog = session.execute(stmt).scalars().first()
        if blog:
            return blog
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found.")
    finally:
        session.close()

@app.post("/blog", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
def create_blog(body: BlogRequest):
    session = SessionFactory()
    try:
        new_blog = Blog(title=body.title, content=body.content)
        session.add(new_blog)
        session.commit()
        return new_blog
    finally:
        session.close()

@app.patch("/blog/{id}", response_model=BlogResponse, status_code=status.HTTP_200_OK)
def update_blog(id: int,body: BlogUpdateRequest):
    session = SessionFactory()
    try:
        stmt = select(Blog).where(Blog.id == id)
        blog = session.execute(stmt).scalars().first()
        if blog:
            if body.title is not None:
                blog.title = body.title
            if body.content is not None:
                blog.content = body.content
            session.commit()
            return blog
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found.")
    finally:
        session.close()
@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int):
    session = SessionFactory()
    try:
        stmt = select(Blog).where(Blog.id == id)
        blog = session.execute(stmt).scalars().first()
        if blog:
            session.delete(blog)
            session.commit()
            return
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found.")
    finally:
        session.close()
