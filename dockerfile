from python:3.12.9

workdir /app

copy requirements.txt .

run pip install --upgrade pip setuptools wheel
run pip install -r requirements.txt
RUN apt-get update && apt-get install -y ca-certificates


copy . .

expose 8000

cmd ["python", "manage.py", "runserver", "0.0.0.0:8000"]