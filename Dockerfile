FROM dustynv/jetson-inference:r32.6.1 as base

RUN apt-get update && apt-get install -y vim
RUN pip3 install --upgrade pip && pip3 install pyserial
