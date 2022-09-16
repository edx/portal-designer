FROM ubuntu:focal as app
MAINTAINER sre@edx.org

RUN apt-get update && apt-get -qy install --no-install-recommends \
 language-pack-en \
 locales \
 python3.8 \
 python3-pip \
 libmysqlclient-dev \
 libssl-dev \
 python3-dev \
 gcc


RUN pip install --upgrade pip setuptools
# delete apt package lists because we do not need them inflating our image
RUN rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV DJANGO_SETTINGS_MODULE {{portaldesigner.project_name}}.settings.production

EXPOSE {{portaldesigner.port}}
RUN useradd -m --shell /bin/false app

WORKDIR /edx/app/{{portaldesigner.repo_name}}

# Copy the requirements explicitly even though we copy everything below
# this prevents the image cache from busting unless the dependencies have changed.
COPY requirements/production.txt /edx/app/{{portaldesigner.repo_name}}/requirements/production.txt

# Dependencies are installed as root so they cannot be modified by the application user.
RUN pip install -r requirements/production.txt

RUN mkdir -p /edx/var/log

# Code is owned by root so it cannot be modified by the application user.
# So we copy it before changing users.
USER app

# Gunicorn 19 does not log to stdout or stderr by default. Once we are past gunicorn 19, the logging to STDOUT need not be specified.
CMD gunicorn --workers=2 --name {{portaldesigner.repo_name}} -c /edx/app/{{portaldesigner.repo_name}}/{{portaldesigner.project_name}}/docker_gunicorn_configuration.py --log-file - --max-requests=1000 {{portaldesigner.project_name}}.wsgi:application

# This line is after the requirements so that changes to the code will not
# bust the image cache
COPY . /edx/app/{{portaldesigner.repo_name}}
