# pull official base image
FROM python:3.10-bullseye

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /temp/requirements.txt
COPY . /app

EXPOSE 8000

# Library for pdf file generation
RUN apt-get update && apt-get install -y xvfb libfontconfig wkhtmltopdf

# install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /temp/requirements.txt
