FROM python:3

#RUN python manage.py collectstatic --noinput

RUN apt-get update && apt-get install -y npm
RUN pip install pipenv --upgrade

COPY Pipfile Pipfile.lock package.json /app/
WORKDIR /app

RUN pipenv install --system

COPY bin /app/bin

RUN npm install
RUN chmod +x bin/update_assets.sh
RUN bin/update_assets.sh

COPY . /app

RUN chmod +x bin/entrypoint.sh

ENTRYPOINT [ "bin/entrypoint.sh" ]

EXPOSE 8000
CMD [ "python", "manage.py",  "runserver", "0.0.0.0:8000" ]
