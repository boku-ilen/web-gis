# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install gdal-bin --yes
COPY . /code/
COPY entrypoint.sh /home/docker/entrypoint.sh
CMD ["/home/docker/entrypoint.sh"]
