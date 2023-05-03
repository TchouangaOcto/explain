FROM python:3.9
RUN pip install --upgrade pip
RUN mkdir /db-data
WORKDIR /explain
COPY . /explain



