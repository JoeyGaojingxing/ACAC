FROM python:3.7-slim
LABEL maintainer="Mojerro <mojerro@163.com>"
WORKDIR /site/
ADD . /site/

ENV FLASK_APP=acac
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD ["/bin/bash"]