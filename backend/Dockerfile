FROM python:latest
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code/
COPY requirements.txt /code/

RUN pip3 install -r requirements.txt
                                      
RUN mkdir /code/bundles/

COPY . /code/

