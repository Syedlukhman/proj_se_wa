FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir flask flask-sqlalchemy flask-login
EXPOSE 5000
CMD ["python", "app.py"]
