FROM nikolaik/python-nodejs:python3.9-nodejs16

RUN apt update && apt upgrade -y
RUN apt install ffmpeg -y

RUN mkdir /app/
COPY . /app
WORKDIR /app
RUN pip3 install pip && pip3 install --upgrade pip && pip3 install -U -r requirements.txt

CMD python3 main.py
