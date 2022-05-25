from typing import Optional
from urllib import response
from fastapi import Body, FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from random import randrange
#pydantic specify how a data should look like
#so that user/frontend knows what data schema should loook like 
app = FastAPI()

class Post(BaseModel):
    # validation
    Title: str
    Content: str
    published: bool = True # default value
    rating: Optional[int] = None#optional parameter
#The GET method is used to retrieve information from the given server using a given URI. Requests using
# GET should only retrieve data and should have no other effect on the data.

#We have not started databases so we will save our data in memory using variables
myPosts = [{"Title": "Title1","Content":"Content1","id":1},{"Title": "Title2","Content":"Content2","id":2}]
@app.get("/")
# this decorator converts your code to an API
# Http request method , get which means we have to send something
# Next we pass the path here it is the root path
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def getPost():
    return {"data": myPosts}

# For POST method the frontend sends the data to the API server
# GET request is like hey server API send me some data.
'''
one way to use post
@app.post("/createposts")
def createPßosts(payload: dict = Body(...)):
    print(payload)
    return {"new post": f"title {payload['Title']} content: {payload['Contents']}"}
'''
#Second way
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPosts(Post:Post):
    #newpost is a pydantic model
    #if you want to convert to a dict use newpost.dict()
    #print(Post.Title,Post.published,Post.rating)
    #print(Post.dict())
    postdict = Post.dict()
    postdict['id'] = randrange(0,1000000)
    myPosts.append(postdict)
    return {"data": postdict}
#Title should be str, content should be str

#API standard convenstions 
#Create use POST eg @app.post("/posts")
#Read use GET eg @app.get("/posts/{id}") and @app.get("/posts/{id}") 
#Update PUT/PATCH Patch is for only single content/field,put needs all the info again that is all the fields @app.put("/posts/{id}")
#Delete DELETE @app.delete("/posts/{id}")
def findPost(id):
    for p in myPosts:
        if p["id"] == id:
            return p


@app.get("/posts/{id}")
def getpost(id:int , response: Response):# this will automatically convert to int and if str is passed it will give a well written error
    print(id)
    #return {"Post" : findPost(int(id))}
    if not findPost(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
    return {"Post" : findPost(id)}


def findIndexPost(id):
    for i,p in enumerate(myPosts):
        if p['id'] == id:
            return i


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id : int):
    index =findIndexPost(id)

    myPosts.pop(index)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def updatePost(id: int, post: Post):
    index = findIndexPost(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Not found')
    postDict = post.dict()
    postDict['id'] = id
    myPosts[index] = postDict
    return {'message': "Updated post"}