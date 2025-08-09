FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

CMD ["gunicorn", "python manage.py migrate && stripepay.wsgi:application", "--bind", "0.0.0.0:8000"]