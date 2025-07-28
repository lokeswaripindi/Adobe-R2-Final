FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    libglib2.0-0 \
    libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
RUN python -c "from transformers import T5Tokenizer, T5ForConditionalGeneration; T5Tokenizer.from_pretrained('t5-small'); T5ForConditionalGeneration.from_pretrained('t5-small')"

CMD ["python", "main.py"]
