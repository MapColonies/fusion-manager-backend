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
        apt-get -y install --no-install-recommends python3.7\
        python-psycopg2\
        build-essential\
        python3.7-dev\
        libpcre3-dev\
        python3-pip\
        libpcre3\
        g++

# Upgrade pip
RUN python3.7 -m pip install --upgrade --force pip

RUN pip install setuptools

# Install django and additional libraries
RUN pip install django\
        djangorestframework\
        django-rest-swagger\
        django-cors-headers\
        dj_database_url\
        psycopg2-binary\
        whitenoise\
        xmltodict\
        xmljson\
        Pillow\
        uwsgi

# Copy source files
COPY geefusion_project_server /opt/myapp/geefusion_project_server

FROM alpine:3.15

COPY --from=base / /

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh

WORKDIR /opt/myapp/geefusion_project_server

EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["bash", "/entrypoint.sh"]
