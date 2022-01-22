FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PORT 8000

ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app/src

RUN apt-get update && apt-get install build-essential curl -y
RUN pip3 install -U pip
RUN pip3 install --upgrade pip
ADD requirements.txt ./
RUN pip3 install -r requirements.txt && \
    apt-get --purge autoremove build-essential -y

COPY src/ ./

EXPOSE 8000
