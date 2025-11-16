import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Request, status
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
import base64

# import celery app instance and the task from worker
from celery_worker import celery_app, process_image_task
from celery.result import AsyncResult

MAX_FILE_SIZE =  16 * 1024 * 1024  # 16 MB Image Size Limit


app = FastAPI()

# allowed CORS origins
origins = [
    "https://no-backdrop-h7sk-kaziseans-projects.vercel.app",
    "https://no.hossain.cc",
    "https://nobackend.hossain.cc",
    "http://localhost",
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# home info
@app.get("/")
async def root():
    return {"message": "Please See /docs for more info"}


@app.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def uploadFile(request: Request, file : UploadFile = File(...)):

    # validate : file type
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a PNG or JPEG image.",
        )

    # Read file in chunks to prevent memory issues
    file_data = await file.read()
    
    # validate :  file size
    if len(file_data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds the limit of {MAX_FILE_SIZE // (1024 * 1024)} MB.",
        )
    
    try :
        # pass the raw bytes of the file to
        # the Celery worker
        task = process_image_task.delay(file_data)

        return {"job_id": task.id, "status": "processing"}
        
    except Exception as e:
        logging.error(f"Error dispatching image to Celery worker: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while queuing the image for processing."
        )

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    """
    status for a job
    If 'PENDING' or 'STARTED', returns status
    If 'FAILURE', returns error
    If 'SUCCESS', returns the processed image file
    """

    task_result = AsyncResult(job_id, app=celery_app)

    if task_result.status == 'FAILURE':
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {
                "status": "error",
                "message": str(task_result.info)
            }
        )
    elif task_result.state == 'SUCCESS':
        try :
            # get base64 of the processed image
            base64_image_string = task_result.get()

            # decode base64 image into bytes
            image_bytes = base64.b64decode(base64_image_string)
            imageIO = BytesIO(image_bytes)
            imageIO.seek(0)
            
            return StreamingResponse(
                imageIO, 
                media_type="image/png",
                headers = {
                    "Content-Disposition": f"attachment; filename=result_{job_id}_nobg.png"
                    }
            )
        except Exception as e:
            logging.error(f"Error decoding/serving processed image: {e}")
            return JSONResponse(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                content = {
                    "status": "error", 
                    "message": "Failed to decode or serve the processed image."
                    }
            )
    return {
        "status": task_result.state.lower()
    }
