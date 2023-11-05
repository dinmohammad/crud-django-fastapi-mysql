from datetime import datetime
import imghdr
import os

from fastapi import HTTPException



async def insert_image(file, IMAGEDIR, BASE_URL):
    currentDate = datetime.today()
    formatted_date = currentDate.strftime("%Y-%m-%d_%H-%M-%S-%f")

    contents = await file.read()
    localImagePath = f'{formatted_date}' + f'{file.filename}'
  
    with open(os.path.join(IMAGEDIR, localImagePath), "wb") as f:
        f.write(contents)
    
    formate_file_name = BASE_URL + IMAGEDIR + f'{formatted_date}' + file.filename 
    return formate_file_name

async def validete_image_formate(file):
    ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}
    file_ext = os.path.splitext(file.filename)[1]
    if file_ext.lower() not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Allowed formats are: jpg, jpeg, png, gif",
        )
        