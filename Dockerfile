FROM python:3.9
ENV PYTHONUNBUFFERED=1
RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean \
&& apt-get install gunicorn3 -y \
&& apt-get install python3.9-dev -y \
&& apt-get install libcurl4-gnutls-dev librtmp-dev -y \
&& apt-get install libnss3 libnss3-dev -y \
&& apt-get install -y cron
RUN touch /var/log/seq.log
WORKDIR /code
COPY requirements.txt /seq_sparky/
RUN pip install -r requirements.txt
COPY . /seq_sparky/

EXPOSE 8000
EXPOSE 8001