FROM python:stretch

COPY . /app
WORKDIR /app

RUN pip install pyjwt
RUN pip install flask
RUN pip install gunicorn
RUN pip install pytest

CMD ["gunicorn","-b",":8080","main:APP"]