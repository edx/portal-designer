FROM python:3.5
WORKDIR /edx/app/portal_designer/portal_designer
ADD requirements.txt /edx/app/portal_designer/portal_designer/
ADD Makefile /edx/app/portal_designer/portal_designer/
ADD requirements/ /edx/app/portal_designer/portal_designer/requirements/
RUN make requirements
ADD . /edx/app/portal_designer/portal_designer
EXPOSE 18808
