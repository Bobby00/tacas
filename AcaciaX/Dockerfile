FROM python:3.8-slim-buster

MAINTAINER Padu 

WORKDIR /home/app

COPY requirements.txt ./ 

RUN pip install -U pip && pip install -r requirements.txt

COPY ./ ./

EXPOSE 8000

# ENTRYPOINT ["gunicorn"]
CMD ["gunicorn", "-b 0.0.0.0:8000", "-w 3", "AcaciaX.wsgi:application"]
