FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --default-timeout=2000 --no-cache-dir -r requirements.txt


COPY . .

# Download the model from Google Drive
RUN python download_model.py

EXPOSE 5000

CMD ["python", "app.py"]
