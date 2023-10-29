import os
from fastapi import FastAPI, File, HTTPException, Depends, Request, UploadFile, status,Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Annotated, Optional
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


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

IMAGEDIR = "uploads/"

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
    stdCls: str = Form(...), 
    details: str = Form(...), 
    user_id: int = Form(...), 
    file: UploadFile = File(...)):
       
    contents = await file.read()
    with open(os.path.join(IMAGEDIR, file.filename), "wb") as f:
        f.write(contents)
    
    db_post = models.student(
        name=name,
        stdCls=stdCls,
        details=details,
        imageUrl=file.filename, 
        user_id=user_id
    )   
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {"Result": "OK"}
    


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
    post_data = db.query(models.student).filter(models.student.user_id == user_id).all()  # // 5 is user id
    if not post_data:
        raise HTTPException(status_code=404, detail='No posts found')
    return post_data

@app.put("/update-student/{std_id}", status_code=status.HTTP_200_OK)
def update_student(std_id: int, student: UpdateStudentBase, db: db_dependency):
    student_db = db.query(models.student).filter(models.student.id == std_id).first()
    if student_db is None:
        raise HTTPException(status_code=404, detail="Student not found")

    if student.name is not None:
        student_db.name = student.name
    if student.stdCls is not None:
        student_db.stdCls = student.stdCls
    if student.details is not None:
        student_db.details = student.details

    db.commit()
    db.refresh(student_db)

    return student_db


@app.delete("/delete-post/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post_by_id(post_id: int, db: db_dependency):
    data = db.query(models.student).filter(models.student.id == post_id).first()
    if data is None:
        raise HTTPException(status_code=404, detail='No posts found')
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
