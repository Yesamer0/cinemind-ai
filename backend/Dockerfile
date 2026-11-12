FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1 NLTK_DATA=/usr/local/share/nltk_data
COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir torch==2.13.0 --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && python -m nltk.downloader -d "$NLTK_DATA" wordnet
COPY backend/app backend/app
COPY backend/evaluate.py backend/evaluate.py
COPY dataset/eval/queries.json dataset/eval/queries.json
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
