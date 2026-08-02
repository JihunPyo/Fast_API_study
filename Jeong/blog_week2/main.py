from fastapi import FastAPI, status, HTTPException
from schema.request import BlogRequest, BlogUpdateRequest
from schema.response import BlogResponse

app = FastAPI()

blogs=[{"id": 1, "title": "First Blog", "content": "This is the first blog content."},
       {"id": 2, "title": "Second Blog", "content": "This is the second blog content."},
       {"id": 3, "title": "Third Blog", "content": "This is the third blog content."}]

@app.get("/blog", response_model=list[BlogResponse], status_code=status.HTTP_200_OK)
def get_blog():
    return blogs

@app.get("/blog/{id}", response_model=BlogResponse, status_code=status.HTTP_200_OK)
def get_blog_id(id: int):
    for blog in blogs:
        if blog["id"]==id:
            return blog
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found.")

@app.post("/blog", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
def create_blog(body: BlogRequest):
    new_blog = {"id": len(blogs) + 1, "title": body.title, "content": body.content}
    blogs.append(new_blog)
    return new_blog

@app.patch("/blog/{id}", response_model=BlogResponse, status_code=status.HTTP_200_OK)
def update_blog(id: int,body: BlogUpdateRequest):
    for blog in blogs:
        if blog["id"]==id:
            blog.update(body.model_dump(exclude_unset=True))
            return blog
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found.")

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int):
    for blog in blogs:
        if blog["id"]==id:
            blogs.remove(blog)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found.")
