FROM python:3.12-slim
LABEL authors="bioan"
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py main.py
COPY enums.py enums.py
COPY models.py models.py

COPY middleware ./middleware
COPY repository ./repository
COPY router ./router
COPY service ./service

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]