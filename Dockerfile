FROM python:3.12
LABEL authors="Erik-Donath"

RUN apt-get update
RUN apt-get install -y locales
RUN echo "de_DE.UTF-8 UTF-8" > /etc/locale.gen
RUN locale-gen de_DE.UTF-8
RUN update-locale LANG=de_DE.UTF-8

ENV LANG=de_DE.UTF-8
ENV LANGUAGE=de_DE:de
ENV LC_ALL=de_DE.UTF-8

WORKDIR /bot
VOLUME  /bot/config
RUN mkdir -p /bot/config

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT ["python3", "Run.py"]
