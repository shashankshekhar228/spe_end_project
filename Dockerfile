FROM python:3.11

COPY . /myapp
WORKDIR /myapp

RUN pip3 install -r requirements.txt --break-system-packages

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1-mesa-glx

EXPOSE 5000
CMD ["python3", "app.py"]