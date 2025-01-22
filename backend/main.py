from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import mimetypes
from io import BytesIO
import os
from rembg import remove
from PIL import Image
from PIL import ImageFilter
import numpy as np


MAX_FILE_SIZE =  16 * 1024 * 1024  # 16 MB Image Size Limit

# init App
app = FastAPI()

# CORS Origins 
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000"
]

# Add CORSMiddleware to allow CORS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
async def root():
    return {"message": "Please See https://no.hossain.cc/docs for more info"}


@app.post("/upload")
async def uploadFile(request: Request, file : UploadFile = File(...)):
    
    # debug delete later
   # origin = request.headers.get('origin')
 #   print(f"Request Origin: {origin}")
    
    # validate file 
    mime_type, _ = mimetypes.guess_type(file.filename)

    if mime_type not in ["image/png", "image/jpeg", "image/jpg"]:
        return {"error": f"Unsupported File type: {mime_type}"}
    
    # if empty 
    if not file : 
        return {"error" : "No files were uploaded"}
    
    # validate file size 
    fileSize = len (await file.read())
    
    if fileSize > MAX_FILE_SIZE:
        raise HTTPException(
            status_code= 400,
            detail=f"File size exceeds the limit of {MAX_FILE_SIZE // (1024 * 1024)} MB. Max file size is 16 MB",
        )
    
    # process the image
    try : 
        usrImage = Image.open(file.file)
        outImage = remove(usrImage, alpha_matting=True)
        
        # enhance 
       # outImage = outImage.filter(ImageFilter.EDGE_ENHANCE)
        
        
        # Save image 
        imageIo = BytesIO()
        outImage = outImage.convert("RGBA")  # Ensure it's in RGBA format (if it's not)
        outImage.save(imageIo, "PNG")
        imageIo.seek(0)
        
        # return no background image
        return StreamingResponse(imageIo, media_type="image/png", headers={"Content-Disposition" : "attachment; filename =_nobg.png"})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail = "An error has occurred on our side. Sorry for any inconvenience." )
