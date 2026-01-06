from fastapi import FastAPI,Response, status, HTTPException
from typing import Optional, Union

from fastapi.params import Body
from pydantic import BaseModel
from random import randrange 
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()
    
class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:

    try: 
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='admin',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as error:
        print('Connecting to database failed')
        print('Error: ', error)
        time.sleep(2)
    
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
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    print(f'Post.......{posts}')
    return {"data": posts}
    
    
@app.post('/posts',status_code=status.HTTP_201_CREATED)
def creat_posts(new_post: PostModel):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s,%s, %s) RETURNING * """,
                   (new_post.title,new_post.content,new_post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'data': new_post}

@app.get('/posts/{id}')
def get_post(id:int, response: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id=%s """,(id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'pst with id {id} not found')
    return {'post_details': post}


@app.delete('/posts/{id}')
def delete_post(id:int):
    # delete post 
    cursor.execute(""" DELETE FROM posts WHERE id=%s returning * """,(id,))
    delete_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post {id} does not exist')
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

@app.put('/posts/{id}')
def update_post(id:int,post:PostModel):
    cursor.execute(
        """ 
        UPDATE posts 
        SET title =%s, content=%s, published=%s 
        WHERE id = %s
        returning id
        """,
        (post.title,post.content,post.published,id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post {id} does not exist')
    return {'data': updated_post}
                
