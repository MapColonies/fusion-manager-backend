FROM ubuntu:16.04 AS base

RUN mkdir -p /opt/myapp

WORKDIR /opt/myapp

# Update repositories
RUN apt-get update
RUN echo Y | apt install software-properties-common

# Add python repository
RUN add-apt-repository ppa:deadsnakes/ppa

# Install dependencies
RUN apt-get update &&\
	apt-get -y install --no-install-recommends sudo\
        python3.7\
        python3-pip\
        python-psycopg2\
        build-essential\
        python3.7-dev\
        g++\
        libpcre3\
        libpcre3-dev\
        nano

# Upgrade pip
RUN python3.7 -m pip install --upgrade --force pip

RUN pip install setuptools

# Install django
RUN pip install django djangorestframework django-rest-swagger django-cors-headers

# Install additional libraries
RUN pip install Pillow xmljson xmltodict dj_database_url psycopg2-binary uwsgi whitenoise

#RUN adduser --disabled-password myuser
#USER myuser

# Copy source files
COPY geefusion_project_server /opt/myapp/geefusion_project_server

FROM alpine
COPY --from=base / /

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh

WORKDIR /opt/myapp/geefusion_project_server

EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["bash", "/entrypoint.sh"]
#ENTRYPOINT ["python3.7", "manage.py", "runserver", "0.0.0.0:8000"]
#ENTRYPOINT ["uwsgi", "--ini", "geefusion_project_server/wsgi-docker.ini"]
