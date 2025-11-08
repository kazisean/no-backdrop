FROM python:3.9-slim

# create a non-root user and group
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# set app work directory
WORKDIR /app

# copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# create and download model
RUN mkdir -p /home/appuser/.u2net
ADD https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx /home/appuser/.u2net/u2net.onnx

# Copy rest of the application files
COPY . .

# give ownership of all files to our new user
RUN chown -R appuser:appgroup /app /home/appuser

# switch to the new non-root user
USER appuser

# port 
EXPOSE 8080

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
