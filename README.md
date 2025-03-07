# Project Title

A short description of your project goes here.

## Table of Contents

- [Project Title](#project-title)
  - [Table of Contents](#table-of-contents)
  - [Non Dockerized Installation](#non-dockerized-installation)
  - [Non Dockerized Usage](#non-dockerized-usage)
  - [Dockerized installation](#dockerized-installation)
  - [Dockerized Usage](#dockerized-usage)
  - [Contributing](#contributing)
  - [License](#license)

## Achievements

All "User functionalities" implemented
Code lenght shortened by usage of external libraries, for example, allauth for user authentification.
Required test coverage of 90% reached. Total coverage: 92.68%
Dockerized and non dockerized execution
Logging

## Non Dockerized Installation

0. Prequisites:

- PostgreSQL
- Virtual enviroment

1. Clone the repository:

```bash
 git clone https://github.com/Diegoolei/todo-challenge
 cd todo-challenge
 pip install -r requirements.txt
```

2. Execute the postgresql database creation script:

```bash
  sudo -u postgres psql -f pg_database.sql
```

3. Create corresponding env file:

- Using .example.env.local as reference, create a file called ".env.local" in the root of the project.

4. Execute django commands:

```bash
  python manage.py collectstatic --noinput
  python manage.py migrate --noinput
```

5. Create django superuser:

```bash
  python manage.py createsuperuser
```

And follow the instructions from de CMD

## Non Dockerized Usage

To run the project, use the following command:

```bash
  gunicorn --bind 0.0.0.0:8000 todolist.wsgi
```

Then, the server will be running at localhost:8000

## Dockerized installation

1. Prequisites:

- Docker

2. Clone the repository:

```bash
 git clone https://github.com/Diegoolei/todo-challenge
 cd todo-challenge
```

3. Create corresponding env file:

- Using .example.env.prod as reference, create a file called ".env.prod" in the root of the project.

4. Build docker image with privilages:

```bash
  sudo docker compose build
```

## Dockerized Usage

To run the project, use the following command with privilages:

```bash
  sudo docker compose up
```

Then, the server will be running at localhost:8001
Finally, create the superuser account by executing:

```bash
  sudo docker compose run django-web python manage.py createsuperuser
```

## Documentation

While the server is running, direct to the [swagger documentation endpoint](http://127.0.0.1:8001/api/docs/) or execute the command

```bash
  python manage.py spectacular --file schema.json
```

and upload the generated file as a [postman collection](https://learning.postman.com/docs/getting-started/importing-and-exporting/importing-and-exporting-overview/#importing-data-into-postman)

## Tests

To run all the tests, execute the following command:

```bash
  tox
```

if running in docker instance:

```bash
sudo docker compose run --rm django-web tox
```

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes.
4. Push your branch: `git push origin feature-name`.
5. Create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

![Build Status](https://travis-ci.org/yourusername/yourproject.svg?branch=main)
