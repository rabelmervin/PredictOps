FROM python:3.10-slim
WORKDIR /app
COPY app/ app/
COPY models/ models/
COPY requirements.txt app/requirements.txt
RUN pip install --no-cache-dir -r app/requirements.txt gunicorn
EXPOSE 5000
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app.app:app"]

