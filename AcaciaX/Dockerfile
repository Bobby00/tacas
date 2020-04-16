ARG BASE_IMAGE=python:3.8-slim-buster
FROM $BASE_IMAGE

MAINTAINER Padu 

WORKDIR /home/app

COPY requirements.txt ./ 

RUN apt-get update && apt-get install -y libpq-dev gcc && \
	pip install -U pip && pip install -r requirements.txt

COPY ./ ./

EXPOSE 8000

# ENTRYPOINT ["gunicorn"]
CMD ["gunicorn", "-b 0.0.0.0:8000", "-w 3", "AcaciaX.wsgi:application"]
