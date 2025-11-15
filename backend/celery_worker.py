import os
import logging
import base64

from io import BytesIO
from rembg import remove
from celery import Celery
from PIL import Image

# TODO: later get redis urls from enviroment variables, with defaults
broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

# max image size for now
MAX_IMAGE_PIXELS = 20 * 1000 * 1000 # 20 megapixels


# celery config
app = Celery (
    'worker',
    broker = broker_url,
    backend = result_backend
)

app.conf.update (
    task_serializer = 'json',
    accept_content = ['json'],
    result_serializer = 'json',
    timezone = 'UTC',
    enable_utc = True,

    # timeout for task 
    task_time_limit = 300, # 5 minutes
    task_soft_limit = 240 # 4 minutes
)

@app.task(name="create_process_image_task")
def process_image_task(image_data_bytes):
    """
    Celery task to remove background from an image
    Receives the image as bytes, returns processed image as a base64 string
    """
    
    try :
        # PIL image size limit
        Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS

        # open image from bytes
        usrImage = Image.open(BytesIO(image_data_bytes))

        # Decompression bomb check
        if usrImage.width * usrImage.height > MAX_IMAGE_PIXELS:
            raise ValueError(f"Image resolution exceeds the limit of {MAX_IMAGE_PIXELS // 1000000} megapixels.")

        # process the image 
        outImage = remove(usrImage)

        # save process image as bytes in memory as bytes
        imageIo = BytesIO()
        outImage.save(imageIo, "PNG")
        imageIo.seek(0)

        # encode as base64 and store in redis
        image_bytes = imageIo.getvalue()
        base64_string = base64.b64encode(image_bytes).decode('utf-8')

        return base64_string

    except Exception as e :
        logging.error(f"Error processing image in celery: {e}")
        # re-raise the exception so Celery marks the task as 'FAILURE'
        # and stores the error message
        raise e
