FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
RUN mkdir /data

# COPY requirements.txt /app
# RUN pip install -r /app/requirements.txt

# Installing dependencies one at a time should make it
# build faster, right?
RUN pip install flask
RUN pip install pyyaml

RUN mkdir /app/testserver
COPY testserver app/testserver

WORKDIR /app/testserver

CMD ["python", "server.py"]
