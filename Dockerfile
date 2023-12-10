FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate; python manage.py loaddata fixtures/categories.json; python manage.py loaddata fixtures/products.json; python manage.py runserver 0.0.0.0:8000"]
