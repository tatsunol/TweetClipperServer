FROM ubuntu:16.04

MAINTAINER tatsunode

WORKDIR /var/www

RUN apt update && \
	apt upgrade -y && \
	apt install -y \
	git \
	python3 \
	python3-pip \
	apache2 \
	libapache2-mod-wsgi-py3

RUN git clone https://github.com/tatsunode/TweetClipperServer && \
	python3 -m pip install -r TweetClipperServer/requirements.txt

ADD apache.conf /etc/apache2/sites-enabled/000-default.conf

EXPOSE 80

CMD ["apachectl", "-D", "FOREGROUND"]
