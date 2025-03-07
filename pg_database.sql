CREATE DATABASE invera_todo;
CREATE DATABASE invera_todo_test;

CREATE USER invera
WITH
    PASSWORD 'invera';

GRANT ALL PRIVILEGES ON DATABASE invera_todo TO invera;
GRANT ALL PRIVILEGES ON DATABASE invera_todo_test TO invera;

ALTER DATABASE invera_todo OWNER TO invera;
ALTER DATABASE invera_todo_test OWNER TO invera;