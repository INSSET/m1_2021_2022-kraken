FROM python

RUN apt update -y
RUN apt install apache2 -y

COPY gplib /usr/local/lib/gplib
ENV PYTHONPATH=/usr/local/lib/gplib

RUN pip install --upgrade pip
RUN pip install ovh
RUN pip install python-dotenv

WORKDIR /opt/project