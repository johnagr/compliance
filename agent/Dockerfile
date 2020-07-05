FROM python:3.8-buster
COPY . /agent
WORKDIR /agent
RUN pip install -r requirements.txt
EXPOSE 5001
CMD python ./agent.py 
