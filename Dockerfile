FROM ubuntu:focal as app
MAINTAINER sre@edx.org

# Packages installed:

# pkg-config; mysqlclient>=2.2.0 requires pkg-config (https://github.com/PyMySQL/mysqlclient/issues/620)

RUN apt-get update && apt-get -qy install --no-install-recommends \
 language-pack-en \
 locales \
 python3.8 \
 python3-pip \
 libmysqlclient-dev \
 pkg-config \
 libssl-dev \
 python3-dev \
 gcc \
 make


RUN pip install --upgrade pip setuptools
# delete apt package lists because we do not need them inflating our image
RUN rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV DJANGO_SETTINGS_MODULE designer.settings.production

EXPOSE 18808
RUN useradd -m --shell /bin/false app

WORKDIR /edx/app/designer

# Copy the requirements explicitly even though we copy everything below
# this prevents the image cache from busting unless the dependencies have changed.
COPY requirements/production.txt /edx/app/designer/requirements/production.txt

# Dependencies are installed as root so they cannot be modified by the application user.
RUN pip install -r requirements/production.txt

RUN mkdir -p /edx/var/log

# Code is owned by root so it cannot be modified by the application user.
# So we copy it before changing users.
USER app

# Gunicorn 19 does not log to stdout or stderr by default. Once we are past gunicorn 19, the logging to STDOUT need not be specified.
CMD gunicorn --workers=2 --name designer -c /edx/app/designer/designer/docker_gunicorn_configuration.py --log-file - --max-requests=1000 designer.wsgi:application

# This line is after the requirements so that changes to the code will not
# bust the image cache
COPY . /edx/app/designer

# Change into dev app
FROM app as devstack
# Install dependencies as root and revert back to application user
USER root
RUN pip install -r /edx/app/designer/requirements/dev.txt
USER app
