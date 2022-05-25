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
import post,user,auth
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
myPosts = [{"Title": "Title1","Content":"Content1","id":1},{"Title": "Title2","Content":"Content2","id":2}]
@app.get("/")
# this decorator converts your code to an API
# Http request method , get which means we have to send something
# Next we pass the path here it is the root path
async def root():
    return {"message": "Hello World"}




def findPost(id):   
    for p in myPosts:
        if p["id"] == id:
            return p




def findIndexPost(id):
    for i,p in enumerate(myPosts):
        if p['id'] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)