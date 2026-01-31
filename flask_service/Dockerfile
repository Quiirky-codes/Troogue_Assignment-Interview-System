FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire folder into the package directory
COPY . /app/flask_service

CMD ["python", "-m", "flask_service.app"]


