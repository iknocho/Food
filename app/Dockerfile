FROM python:3.11-slim

WORKDIR /app

COPY requirements/requirements.txt ./requirements/
RUN pip install --no-cache-dir -r requirements/requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 