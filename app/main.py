from fastapi import FastAPI,Response, status, HTTPException
from typing import Optional, Union

from fastapi.params import Body
from pydantic import BaseModel
from random import randrange 

app = FastAPI()
    
class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
my_posts = [{"title": "title of post 1", "content":"content of post 1","id":1},
            {"title": "favorite foods", "content":"I like pizza","id":2}]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
        
def find_index_post(id:int):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i



@app.get("/")
def read_root():
    return {"message": "welcome to my api1"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/post")
def get_post():
    return {"data": my_posts}
    
    
@app.post('/posts',status_code=status.HTTP_201_CREATED)
def creat_posts(new_post: PostModel):
    post_dict = new_post.model_dump()
    post_dict['id'] = randrange(1,11111111)
    my_posts.append(post_dict)
    return {'data': post_dict}

@app.get('/posts/{id}')
def get_post(id:int, response: Response):

    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'pst with id {id} not found')
    return {'post_details': post}


@app.delete('/posts/{id}')
def delete_post(id:int):
    # delete post 
    idx = find_index_post(id)
    if idx == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post {id} does not exist')
    my_posts.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

@app.put('/posts/{id}')
def update_post(id:int,post:PostModel):
    print(post)
    idx = find_index_post(id)
    if idx == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post {id} does not exist')
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[idx] = post_dict
    return {'data': post_dict}
                
