FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /code/src/checkloading

COPY pip_requirements.txt /code/src/checkloading
RUN pip install --no-cache-dir -r pip_requirements.txt

COPY . /code/src/checkloading

EXPOSE 8000

ENV SECRET_KEY "django-insecure-1smtc!loc!aa-r0t2t=(j8u#(09!f()j4)6q4u%q@ujge7t^@s"
ENV DJANGO_SETTINGS_MODULE "checksloading.settings"
ENV DB_ENGINE "django.db.backends.postgresql"
ENV DB_NAME "checkloading_db"
ENV DB_USER "anton"
ENV DB_PASSWORD "pass"
ENV DB_HOST "checkloading_db"
ENV DB_PORT "5432"