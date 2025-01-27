from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from rembg import remove
from PIL import Image



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

# Home Page info
@app.get("/")
async def root():
    return {"message": "Please See /docs for more info"}


# Upload function
@app.post("/upload")
async def uploadFile(request: Request, file : UploadFile = File(...)):

    # read given file 
    file_data = await file.read()
    
    # validate : if empty 
    if not file : 
        raise HTTPException(
            status_code= 400,
            detail=f"No files were uploaded.",
        )
    
    # validate :  file size 
    if len(file_data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds the limit of {MAX_FILE_SIZE // (1024 * 1024)} MB.",
        )
    
    # process the image
    try : 
        usrImage = Image.open(BytesIO(file_data))
        outImage = remove(usrImage)
        
        # save image 
        imageIo = BytesIO()
        outImage.save(imageIo, "PNG")
        imageIo.seek(0)
        
        # return no background image
        return StreamingResponse(imageIo, media_type="image/png", headers={"Content-Disposition" : "attachment; filename =_nobg.png"})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail = "An error has occurred on our side. Sorry for any inconvenience." )
