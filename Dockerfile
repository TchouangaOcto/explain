FROM python:3.9
RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN mkdir /db-data
WORKDIR /explain
COPY . /explain



