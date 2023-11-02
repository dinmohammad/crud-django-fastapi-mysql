from datetime import datetime
import os



async def insert_image(file, IMAGEDIR, BASE_URL):
    currentDate = datetime.today()
    formatted_date = currentDate.strftime("%Y-%m-%d_%H-%M-%S-%f_")

    contents = await file.read()
    localImagePath = f'{currentDate}' + f'{file.filename}'
  
    with open(os.path.join(IMAGEDIR, localImagePath), "wb") as f:
        f.write(contents)
    
    formate_file_name = BASE_URL + IMAGEDIR + f'{formatted_date}' + file.filename 
    return formate_file_name