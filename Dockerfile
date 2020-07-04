FROM python:3.5
WORKDIR /edx/app/designer
ADD requirements.txt /edx/app/designer/
ADD Makefile /edx/app/designer/
ADD requirements/ /edx/app/designer/requirements/
RUN make requirements

EXPOSE 8808
RUN useradd -m --shell /bin/false app
USER app

CMD gunicorn --bind=0.0.0.0:8808 --workers 2 --max-requests=1000 -c /edx/app/enterprise_catalog/docker_gunicorn_config.py  designer.wsgi:application
ADD . /edx/app/designer
