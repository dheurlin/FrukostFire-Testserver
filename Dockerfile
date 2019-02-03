FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
RUN mkdir /data

WORKDIR /app

# Install mypy for typechecking and entr to
# run mypy automatically when files change
RUN echo "deb http://ftp.debian.org/debian jessie main" >> /etc/apt/sources.list
RUN apt-get update -y && apt-get install -y entr
RUN pip install mypy

RUN pip install flask
RUN pip install pyyaml

RUN mkdir testserver
COPY testserver testserver
COPY entrypoint.sh .

WORKDIR /app/testserver

CMD ["sh", "/app/entrypoint.sh"]
