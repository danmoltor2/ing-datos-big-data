CREATE DATABASE IF NOT EXISTS entrega1;
USE entrega1;

-- Creamos la tabla info_household
DROP TABLE IF EXISTS info_household;
CREATE EXTERNAL TABLE IF NOT EXISTS info_household (
    lclid STRING, 
    stdortou STRING, 
    acorn STRING, 
    acorn_grouped STRING, 
    file STRING
) 
STORED AS PARQUET
LOCATION '/tmp/informations_households.parquet';

-- Creamos la tabla halfhourly
DROP TABLE IF EXISTS halfhourly;
CREATE EXTERNAL TABLE IF NOT EXISTS halfhourly (
    lclid STRING,
    tstp TIMESTAMP,
    energy DOUBLE
) 
STORED AS PARQUET
LOCATION '/tmp/halfhourly_parquet';

-- Refrescamos metadatos
MSCK REPAIR TABLE halfhourly;
