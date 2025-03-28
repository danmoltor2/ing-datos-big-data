-- Creamos el rol hive con contraseña
CREATE ROLE hive WITH LOGIN PASSWORD 'password';

-- Concedemos privilegios sobre la base de datos metastore_db al rol hive
GRANT CONNECT, TEMPORARY, CREATE, SELECT, INSERT, UPDATE, DELETE ON DATABASE metastore_db TO hive;

-- Permitimos que el rol hive pueda crear bases de datos y esquemas
ALTER ROLE hive WITH CREATEDB;
