from typing import Optional
from urllib import response
from fastapi import Body, FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
import time
from psycopg2.extras import RealDictCursor
#pydantic specify how a data should look like
#so that user/frontend knows what data schema should loook like 
from . import models
from .database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):
    # validation
    Title: str
    Content: str
    published: bool = True # default value
while True:

    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',
        password='root', cursor_factory=RealDictCursor)
        cursor = conn.cursor()

        print("database connected")
        break
    except Exception as error:
        print("connection failed")
        print("error was", error)
        time.sleep(2)

    
#We have not started databases so we will save our data in memory using variables
myPosts = [{"Title": "Title1","Coßntent":"Content1","id":1},{"Title": "Title2","Content":"Content2","id":2}]
@app.get("/")
# this decorator converts your code to an API
# Http request method , get which means we have to send something
# Next we pass the path here it is the root path
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def getPost():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

# For POST method the frontend sends the data to the API server
# GET request is like hey server API send me some data.

#Second way
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPosts(Post:Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(Post.Title,Post.Content,Post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

def findPost(id):
    for p in myPosts:
        if p["id"] == id:
            return p


@app.get("/posts/{id}")
def getpost(id:int , response: Response):# this will automatically convert to int and if str is passed it will give a well written error
    cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found")
    return {"Post" : post}


def findIndexPost(id):
    for i,p in enumerate(myPosts):
        if p['id'] == id:
            return i


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id : int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    deleted = cursor.fetchone()
    if deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Not found')
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def updatePost(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title=%s,content =%s,published=%s WHERE id = %s RETURNING *""",(post.Title,post.Content,post.published,str(id)))
    updated_post= cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Not found')
 
    return {'message': updated_post}