FROM python:3.8-buster
COPY . /api
WORKDIR /api
RUN pip3 install -r requirements.txt
RUN apt-get update
RUN apt-get install sqlite3
EXPOSE 5000
CMD python ./api.py 
