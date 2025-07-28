FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    poppler-utils \
    libglib2.0-0 \
    libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip uninstall -y fitz || true
RUN pip install --no-cache-dir PyMuPDF==1.23.7

CMD ["python", "main.py"]

