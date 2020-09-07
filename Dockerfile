ARG PYTHON_IMAGE=python:3.8-buster

FROM ${PYTHON_IMAGE} as friendo_site_dev

RUN apt-get update && apt-get install -y --no-install-recommends gettext

RUN pip install pipenv

RUN mkdir /code
COPY . /code

WORKDIR /code

RUN pipenv install --system --deploy

WORKDIR /code/friendo_site

#RUN python3 manage.py migrate

ENTRYPOINT ["bash"]
