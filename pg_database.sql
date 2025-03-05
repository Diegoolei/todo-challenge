CREATE DATABASE invera_todo;

CREATE USER invera
WITH
    PASSWORD 'invera';

GRANT ALL PRIVILEGES ON DATABASE invera_todo TO invera;

ALTER DATABASE invera_todo OWNER TO invera;