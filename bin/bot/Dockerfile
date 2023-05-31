FROM python:3.8

# don't make .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# not buffer to stdin/stdout
ENV PYTHONUNBUFFERED 1

WORKDIR /opt/app/

COPY ./requirements.txt /opt/app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /opt/app/requirements.txt

COPY . /opt/app/