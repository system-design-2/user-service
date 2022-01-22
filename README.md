## Installation
- run `cp example.env .env` and update .env file with your configuration.
- run `docker-compose up --build`

## Note
- run `docker-compose exec app bash`
- run `./manage.py createsuperuser` in docker container to create a superuser for performing admin task
- run `./manage.py test` in docker container for unit testing
- if everything goes right check the health check url at `http://localhost:8000/api/v1`
- check swagger API documentation at `http://localhost:8000/doc/`
- Employee can vote only one in a day before configure deadline time and result will be published after deadline.