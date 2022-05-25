
from fastapi import FastAPI,Request,Response,status,HTTPException, Depends,APIRouter
from typing import Optional
from sqlalchemy.orm import Session
import sys
import models,schema,oauth2
from  database import get_db
from typing import List

router = APIRouter(prefix="/posts",tags=['Posts'])


@router.get("/",response_model=List[schema.Post])
def getPost(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),limit: int= 10, skip: int=0,
search: Optional[str]=''):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

# For POST method the frontend sends the data to the API server
# GET request is like hey server API send me some data.

#Second way
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def createPosts(post:schema.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    #new_post = models.Post(title = Post.Title, content=Post.Content, published=Post.published)
    
    
    #print(Post.dict())
    new_post= models.Post(owner_id= current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}",response_model=schema.Post)
def getpost(id:int , response: Response, db: Session= Depends(get_db)):# this will automatically convert to int and if str is passed it will give a well written error
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found")
    return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id : int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform the following actions")
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schema.Post)
def updatePost(id: int, post: schema.PostCreate,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    postquery = db.query(models.Post).filter(models.Post.id==id)
    post = postquery.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Not found')
    if post.owner_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform the following actions")

    postquery.update({'title':'hey this is updated','content':'this is my updated' },synchronize_session=False)

    db.commit()

    return  postquery.first()
## Schema/pydantic models define the structure of a request and response.

## This ensure that when a user wants to create a post, the request will only go through 
## if it has a title and content the body.

##Sqlalchemy/ORM modelks--> responsible for defining the columns of our posts table within postfgres
# Is used to query, create, delete and update entries within the database]
