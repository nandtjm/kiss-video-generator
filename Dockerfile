FROM nvidia/cuda:11.8-cudnn8-runtime-ubuntu22.04
WORKDIR /workspace
RUN apt-get update && apt-get install -y python3-pip ffmpeg
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
