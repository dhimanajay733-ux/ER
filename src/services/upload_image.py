from fastapi import UploadFile, HTTPException, status
from uuid import uuid4
from pathlib import Path
from typing import List

def upload_product_images(files: List[UploadFile]):
 
    ALLOWED_MIME_TYPES = {
 
        "image/jpeg": [".jpg", ".jpeg","image/png"],
        "image/png": [
        ".png"
    ]
 
    }

    MAX_FILE_SIZE = 1024 * 1024  # 1 MB
 
    MAX_FILE_COUNT = 5
 
 
    if len(files) > MAX_FILE_COUNT:
 
        raise HTTPException(
 
            status_code=status.HTTP_400_BAD_REQUEST,
 
            detail=f"Maximum {MAX_FILE_COUNT} images are allowed"
 
        )
    uploaded_images = []
 
    upload_dir =  Path(__file__).parents[2] / "static"/ "uploads"/ "products"
 
    upload_dir.mkdir(parents=True, exist_ok=True)
  
    for file in files:
        if file.content_type not in ALLOWED_MIME_TYPES:
 
            raise HTTPException(
 
                status_code=415,
 
                detail=f"File type '{file.content_type}' is not allowed."
 
            )
        extention = Path(file.filename).suffix.lower()

        if extention not in ALLOWED_MIME_TYPES[file.content_type]:
 
            raise HTTPException(
 
                status_code=415,
 
                detail=f"Extension '{extention}' does not match content type."
 
            )
        file.file.seek(0, 2)
 
        file_size = file.file.tell()
 
        file.file.seek(0)
 
        if file_size > MAX_FILE_SIZE:
 
            raise HTTPException(
 
                status_code=413,
 
                detail=f"{file.filename} exceeds 1 MB limit."
            )
        
        safe_name = f"{uuid4().hex}{extention}"
        destination = upload_dir / safe_name
  
        with destination.open("wb") as out_file:
 
            while chunk := file.file.read(1024 * 1024):
 
                out_file.write(chunk)

        uploaded_images.append({
 
            "filename": safe_name,
 
            "image_url": f"/static/uploads/products/{safe_name}"
 
        })
    return {
 
        "message": "Images uploaded successfully",
 
        "images": uploaded_images
 
    }