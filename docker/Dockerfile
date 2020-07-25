FROM ubuntu:20.04

MAINTAINER tatsunode

WORKDIR /var/www

RUN apt update && \
	apt upgrade -y && \
	apt install -y \
	python3 \
	python3-pip \
	apache2 \
	libapache2-mod-wsgi-py3

ADD apache.conf /etc/apache2/sites-enabled/000-default.conf
ADD ../server.py
ADD ../wsgi.py
ADD ../requirements.txt

RUN python3 -m pip install -U pip && \
	python3 -m pip install -r requirements.txt

EXPOSE 80

CMD ["apachectl", "-D", "FOREGROUND"]