FROM python:3.5
WORKDIR /edx/app/designer/designer
ADD requirements.txt /edx/app/designer/designer/
ADD Makefile /edx/app/designer/designer/
ADD requirements/ /edx/app/designer/designer/requirements/
RUN make requirements
ADD . /edx/app/designer/designer
EXPOSE 18808
