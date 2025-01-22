FROM python:3.9

# Install wget to download u2net model
RUN apt-get update && apt-get install -y wget

# Download the u2net.onnx file from the URL
RUN mkdir -p /home/.u2net
RUN wget -O /home/.u2net/u2net.onnx https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# port 
EXPOSE 8080

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
