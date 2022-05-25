from calendar import c
from typing import Optional,List
from urllib import response
from fastapi import Body, Depends, FastAPI,Response,status,HTTPException
from random import randrange
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
#pydantic specify how a data should look like
#so that user/frontend knows what data schema should loook like 
import models,schema
from database import engine, get_db
import utils
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

@app.get("/posts",response_model=List[schema.Post])
def getPost(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# For POST method the frontend sends the data to the API server
# GET request is like hey server API send me some data.

#Second way
@app.post("/posts", status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def createPosts(post:schema.PostCreate, db: Session = Depends(get_db)):
    
    #new_post = models.Post(title = Post.Title, content=Post.Content, published=Post.published)
    
    
    #print(Post.dict())
    new_post= models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def findPost(id):   
    for p in myPosts:
        if p["id"] == id:
            return p


@app.get("/posts/{id}",response_model=schema.Post)
def getpost(id:int , response: Response, db: Session= Depends(get_db)):# this will automatically convert to int and if str is passed it will give a well written error
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found")
    return post


def findIndexPost(id):
    for i,p in enumerate(myPosts):
        if p['id'] == id:
            return i


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id : int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)
    if post.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",response_model=schema.Post)
def updatePost(id: int, post: schema.PostCreate,db:Session = Depends(get_db)):
    postquery = db.query(models.Post).filter(models.Post.id==id)
    post = postquery.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Not found')
    postquery.update({'title':'hey this is updated','content':'this is my updated' },synchronize_session=False)

    db.commit()

    return  postquery.first()
## Schema/pydantic models define the structure of a request and response.

## This ensure that when a user wants to create a post, the request will only go through 
## if it has a title and content the body.

##Sqlalchemy/ORM modelks--> responsible for defining the columns of our posts table within postfgres
# Is used to query, create, delete and update entries within the database]

@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    ## hash password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user =models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users/{id}',response_model=schema.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id== id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {id} does not exist")

    return user