from calendar import c
from typing import Optional,List
from urllib import response
from fastapi import Body, Depends, FastAPI,Response,status,HTTPException
#pydantic specify how a data should look like
#so that user/frontend knows what data schema should loook like 
import models
from database import engine, get_db
import utils
import post,user,auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
    
#We have not started databases so we will save our data in memory using variables
@app.get("/")
# this decorator converts your code to an API
# Http request method , get which means we have to send something
# Next we pass the path here it is the root path
async def root():
    return {"message": "Hello World"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)