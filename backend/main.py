import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from rembg import remove
from PIL import Image

MAX_FILE_SIZE =  16 * 1024 * 1024  # 16 MB Image Size Limit
MAX_IMAGE_PIXELS = 20 * 1000 * 1000 # 20 megapixels

# init App
app = FastAPI()

# Allowed CORS Origins 
origins = [
    "https://no-backdrop-h7sk-kaziseans-projects.vercel.app",
    "https://no.hossain.cc"
]

# Add CORSMiddleware to allow CORS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"], 
    allow_headers=["*"],  # Allow all headers
)

# Home Page info
@app.get("/")
async def root():
    return {"message": "Please See /docs for more info"}


@app.post("/upload")
async def uploadFile(request: Request, file : UploadFile = File(...)):

    # validate : file type
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a PNG or JPEG image.",
        )

    file_data = await file.read()
    
    # validate :  file size
    if len(file_data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds the limit of {MAX_FILE_SIZE // (1024 * 1024)} MB.",
        )
    
    try : 
        Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS
        usrImage = Image.open(BytesIO(file_data))

        # decompression bomb check
        if usrImage.width * usrImage.height > MAX_IMAGE_PIXELS:
            raise HTTPException(
                status_code=400,
                detail=f"Image resolution exceeds the limit of {MAX_IMAGE_PIXELS // 1000000} megapixels.",
            )

        outImage = remove(usrImage)
        
        # save image 
        imageIo = BytesIO()
        outImage.save(imageIo, "PNG")
        imageIo.seek(0)

        return StreamingResponse(imageIo, media_type="image/png", headers={"Content-Disposition" : f"attachment; filename={file.filename}_nobg.png"})
        
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the image.")

