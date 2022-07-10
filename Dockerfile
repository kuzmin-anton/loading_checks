FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /code/src/checkloading

COPY pip_requirements.txt /code/src/checkloading
RUN pip install --no-cache-dir -r pip_requirements.txt

COPY checksloading/ /code/src/checkloading

EXPOSE 8000