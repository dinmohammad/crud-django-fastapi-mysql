from datetime import date
import imghdr
import os
from fastapi import FastAPI, File, HTTPException, Depends, Request, UploadFile, status,Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Annotated, Optional
from core.helper import insert_image, validete_image_formate
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)



BASE_URL = 'http://127.0.0.1:8000/' # port 8000
IMAGEDIR = "uploads/"
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


class UserBase(BaseModel):
    username: str


class postBase(BaseModel):
    title: str
    content: str
    user_id: int

class studentBase(BaseModel):
    name: str
    stdCls: str
    details: str
    imageUrl: Optional[UploadFile] = File(None)
    user_id: int

class UpdateStudentBase(BaseModel):
    name: Optional[str] = None
    stdCls: Optional[str] = None
    details: Optional[str] = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]



@app.post("/image_upload/")
async def image_post(request: Request, file: UploadFile = File(...)):
    contents = await file.read()

    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    print(file.filename)
    return {"Result": "OK"}
   


@app.post("/create_student/", status_code=status.HTTP_201_CREATED)
async def create_post(
    db: db_dependency,
    name: str = Form(...), 
    stdcls: str = Form(...), 
    details: str = Form(...), 
    file: UploadFile = File(...),
    user_id: int = Form(...)):


    file_ext = os.path.splitext(file.filename)[1]
    if file_ext.lower() not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Allowed formats are: jpg, jpeg, png, gif",
        )

    Image_path = await insert_image(file, IMAGEDIR, BASE_URL) # helper.inser_image function use 

    db_post = models.student(
        name=name,
        stdcls=stdcls,
        details=details,
        imageUrl=Image_path, 
        user_id=user_id
    )   
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {"Result": db_post}
    


@app.get("/get_student/{std_id}", status_code=status.HTTP_200_OK)
async def create_post(std_id: int, db: db_dependency):
    post_data = db.query(models.student).filter(models.student.id == std_id).first()
    if post_data is None:
        raise HTTPException(status_code=404, detail='post not found')
    return post_data


@app.get("/all_student/", status_code=status.HTTP_201_CREATED)
async def get_all_posts(db: db_dependency):
    post_data = db.query(models.student).all()
    if not post_data:
        raise HTTPException(status_code=404, detail='No posts found')
    return post_data


@app.get("/all_post_by_user_id/{user_id}", status_code=status.HTTP_201_CREATED)
async def get_all_posts(user_id: int, db: db_dependency):
    post_data = db.query(models.student).filter(models.student.user_id == user_id).all()  # // default 5 is user id
    if not post_data:
        raise HTTPException(status_code=404, detail='No posts found')
    return post_data

@app.put("/update-student/{std_id}", status_code=status.HTTP_201_CREATED)
async def update_student(
    db: db_dependency,
    std_id: int, 
    name: str = Form(...), 
    stdcls: str = Form(...), 
    details: str = Form(...), 
    file: UploadFile = File(...),
    user_id: int = Form(...)
):
    student_db = db.query(models.student).filter(models.student.id == std_id).first()
    if student_db is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if name is not None:
        student_db.name = name
    if stdcls is not None:
        student_db.stdcls = stdcls
    if details is not None:
        student_db.details = details
    if file is not None:
        Image_path = await insert_image(file, IMAGEDIR, BASE_URL) # user helper.insert_image functon
        student_db.imageUrl = Image_path
    if user_id is not None:
        student_db.user_id = user_id

    db.commit()
    db.refresh(student_db)

    return student_db


@app.delete("/delete-post/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post_by_id(post_id: int, db: db_dependency):
    data = db.query(models.student).filter(models.student.id == post_id).first()
    
    if data is None:
        raise HTTPException(status_code=404, detail='No posts found')
    
    image_url = data.imageUrl
    filename = os.path.basename(image_url)
    image_path = os.path.join(IMAGEDIR, filename)

    # Delete the image file from the server if it exists
    if os.path.exists(image_path):
        os.remove(image_path)

    db.delete(data)
    db.commit()



@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()


@app.get("/users/{user_id}", status_code=status.HTTP_201_CREATED)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='user not found')
    return user


