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
0. Prequisites:
  - Docker

1. Clone the repository:
```bash
 git clone https://github.com/Diegoolei/todo-challenge
 cd todo-challenge
```

1. Create corresponding env file:
  - Using .example.env.prod as reference, create a file called ".env.prod" in the root of the project.

2. Build docker image with privilages:
```bash
  sudo docker compose build
```

## Dockerized Usage
To run the project, use the following command with privilages:
```bash
  sudo docker compose up
```

Then, the server will be running at localhost:8001

## Contributing
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes.
4. Push your branch: `git push origin feature-name`.
5. Create a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

![Build Status](https://travis-ci.org/yourusername/yourproject.svg?branch=main)