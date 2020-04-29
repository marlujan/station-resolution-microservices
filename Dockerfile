FROM python:3.7

RUN apt-get update
RUN pip3 install uwsgi pipenv

COPY ./web_application /opt/web_application
COPY uwsgi.ini /opt/uwsgi.ini

WORKDIR /opt/web_application

RUN pipenv install
RUN git clone https://github.com/networktocode/ntc-templates.git ~/ntc-templates

ENTRYPOINT uwsgi /opt/uwsgi.ini -H $(pipenv --venv)

