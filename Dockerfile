FROM python:3.10

WORKDIR /

# Install git
RUN apt-get update && apt-get install -y git

# Install python packages
RUN pip3 install --upgrade pip
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /app

ADD src/. .

WORKDIR /

EXPOSE 80

CMD python3 -u app/server.py