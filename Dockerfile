FROM ubuntu:18.04

# Add user
RUN adduser --quiet --disabled-password qtuser

COPY . . 

# Install Python 3, PyQt5
RUN apt-get update \
    && apt-get install -y \
      python3 \
      python3-pip\
      python3-pyqt5

RUN pip3 install -r requirements.txt