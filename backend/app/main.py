import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Request, status
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
import base64

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# import celery app instance
from app.celery_app import celery_app
from celery.result import AsyncResult

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB Image Size Limit



# allowed CORS origins
origins = [
    "https://no-backdrop-h7sk-kaziseans-projects.vercel.app",
    "https://no.hossain.cc",
    "https://nobackend.hossain.cc",
    "http://localhost",
    "http://localhost:3000",
]

# rate limit implementation
def get_cloudflare_ip(request: Request):
    return request.headers.get("cf-connecting-ip") or request.client.host

limiter = Limiter(
    key_func=get_cloudflare_ip,
    storage_uri="redis://redis:6379/1" # wsing DB 1 to keep it sep from Celery
)

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.middleware("http")
async def cloudflare_proxy_middleware(request: Request, call_next):
    # cloudflare real user ipheader
    real_ip = request.headers.get("cf-connecting-ip")
    request.state.user_ip = real_ip or request.client.host
    
    # log request details for debugging CORS
    origin = request.headers.get("origin", "none")
    method = request.method
    path = request.url.path
    logging.info(f"[CORS DEBUG] {method} {path} from origin: {origin}")
    
    response = await call_next(request)
    
    # log response headers for debugging CORS
    cors_header = response.headers.get("access-control-allow-origin", "NOT SET")
    logging.info(f"[CORS DEBUG] Response CORS header: {cors_header}")
    
    # security header no bypassing the tunnel
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.on_event("startup")
async def startup_event():
    logging.info(f"[CORS CONFIG] Allowed origins: {origins}")
    logging.info(f"[CORS CONFIG] CORS middleware configured with allow_methods: GET, POST, OPTIONS, HEAD")

# home info
@app.get("/")
async def root():
    return {"message": "Please See /docs for more info"}


# health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fastapi-backdrop"}


@app.options("/upload")
async def upload_options(request: Request):
    """Handle CORS preflight requests explicitly"""
    logging.info(f"OPTIONS /upload received from {request.headers.get('origin', 'unknown')}")
    return {"status": "ok"}

@app.post("/upload", status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("5/minute")
async def uploadFile(request: Request, file: UploadFile = File(...)):

    # validate : file type
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a PNG or JPEG image.",
        )

    # read file in chunks to prevent memory issues
    file_data = await file.read()

    # validate :  file size
    if len(file_data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds the limit of {MAX_FILE_SIZE // (1024 * 1024)} MB.",
        )

    # additional validation: check if file is an image for real
    try:
        from PIL import Image
        from io import BytesIO

        test_image = Image.open(BytesIO(file_data))
        test_image.close()
        del test_image
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file. Please upload a valid PNG or JPEG image.",
        )

    try:
        # pass the raw bytes of the file to
        # the Celery worker
        task = celery_app.send_task("create_process_image_task", args=[file_data])

        return {"job_id": task.id, "status": "processing"}

    except Exception as e:
        logging.error(f"Error dispatching image to Celery worker: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while queuing the image for processing.",
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

    if task_result.status == "FAILURE":
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": str(task_result.info)},
        )
    elif task_result.state == "SUCCESS":
        try:
            # get base64 of the processed image
            base64_image_string = task_result.get()

            # decode base64 image into bytes
            image_bytes = base64.b64decode(base64_image_string)
            imageIO = BytesIO(image_bytes)
            imageIO.seek(0)

            # clean up the task result from Redis after retrieving the data
            # this removes the processed image from Redis memory immediately
            task_result.forget()

            return StreamingResponse(
                imageIO,
                media_type="image/png",
                headers={
                    "Content-Disposition": f"attachment; filename=result_{job_id}_nobg.png"
                },
            )
        except Exception as e:
            logging.error(f"Error decoding/serving processed image: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "status": "error",
                    "message": "Failed to decode or serve the processed image.",
                },
            )
    return {"status": task_result.state.lower()}
