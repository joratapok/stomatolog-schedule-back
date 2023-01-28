# pull official base image
FROM python:3.10-bullseye

COPY requirements.txt /temp/requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 8000

# Library for pdf file generation
RUN apt-get update && apt-get install -y xvfb libfontconfig wkhtmltopdf

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /temp/requirements.txt
