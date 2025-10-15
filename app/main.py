from fastapi import FastAPI
from typing import Optional, Union

from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()
    
class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    

@app.get("/")
def read_root():
    return {"message": "welcome to my api1"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/post")
def get_post():
    return {"data": "this is you post",
            "id": '5'}
    
    
@app.post('/posts')
def creat_posts(new_post: PostModel):
    return {'data': new_post.model_dump()}
