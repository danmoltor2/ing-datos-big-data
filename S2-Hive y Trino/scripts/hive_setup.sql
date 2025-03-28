CREATE DATABASE IF NOT EXISTS entrega1;
USE entrega1;

-- Creamos la tabla info_household
DROP TABLE IF EXISTS info_household;
CREATE TABLE IF NOT EXISTS info_household (
    lclid STRING, 
    stdortou STRING, 
    acorn STRING, 
    acorn_grouped STRING, 
    file STRING
) STORED AS PARQUET;

-- Cargamos los datos en la tabla info_household
LOAD DATA LOCAL INPATH '/tmp/informations_households.parquet' OVERWRITE INTO TABLE entrega1.info_household;

-- Creamos la tabla halfhourly
DROP TABLE IF EXISTS halfhourly;
CREATE TABLE IF NOT EXISTS halfhourly (
    lclid STRING,
    tstp TIMESTAMP,
    energy DOUBLE
) STORED AS PARQUET;
