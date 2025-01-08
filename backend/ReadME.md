python -m venv venv 

.\venv\Scripts\activate

pip install "fastapi[standard]"

pip install onnxruntime

pip install pillow
pip install slowapi


uvicorn main:app --reload

using slowapi to rateLimit 

write test cases