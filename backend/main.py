from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import StreamingResponse, FileResponse
from io import BytesIO
from rembg import remove
from PIL import Image
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address


MAX_FILE_SIZE =  16 * 1024 * 1024  # 16 MB Image Size Limit

# init App
app = FastAPI()

# Rate limit
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)


@app.get("/")
async def root():
    return {"message": "Please See https://no.hossain.cc/docs for more info"}


@app.post("/upload")
@limiter.limit("10/minute", key_func=lambda request: request.state.user_role) # rate limit 10 request per ip
async def uploadFile(request: Request, file : UploadFile = File(...)):
    
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
        outImage = remove(usrImage, post_process_mask=True)
        
        # Save image 
        imageIo = BytesIO()
        outImage.save(imageIo, "PNG")
        imageIo.seek(0)
        
        # return no background image
        return StreamingResponse(imageIo, media_type="image/png", headers={"Content-Disposition" : "attachment; filename =_nobg.png"})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail = "An error has occurred on our side. Sorry for any inconvenience." )
