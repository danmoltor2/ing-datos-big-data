# Ejecutamos los scripts para convertir los archivos CSV a Parquet
python scripts/csvToParquet.py

# En Git bash
cd Desktop/Programas/Máster/BD/Proyectos_clase/ing-datos-big-data/S2-Hive\ y\ Trino
./scripts/entrega1-setup.sh

# Una vez finalizado, en otro terminal:
docker exec -it hiveserver2 beeline -u jdbc:hive2://localhost:10000

USE entrega1;

SELECT COUNT(*) AS total_registros FROM info_household;
SELECT COUNT(*) AS total_registros FROM halfhourly;



















# Copiamos los archivos Parquet a la máquina de Docker
docker cp ../datasets/E1/informations_households.parquet hiveserver2:/tmp/informations_households.parquet
docker cp ../datasets/E1/halfhourly_parquet hiveserver2:/tmp/halfhourly_parquet

# Creamos la base de datos y la tabla con cada una de sus columnas:
create database entrega1;
USE entrega1;
CREATE TABLE IF NOT EXISTS info_household (lclid STRING, stdortou STRING, acorn STRING, acorn_grouped STRING, file STRING) STORED AS PARQUET;
LOAD DATA LOCAL INPATH '/tmp/informations_households.parquet' OVERWRITE INTO TABLE entrega1.info_household;

# Repetimos el proceso para la tabla halfhourly
CREATE TABLE IF NOT EXISTS halfhourly (lclid STRING,tstp TIMESTAMP,energy DOUBLE) STORED AS PARQUET;
LOAD DATA LOCAL INPATH '/tmp/halfhourly_parquet/' OVERWRITE INTO TABLE entrega1.halfhourly;

#Comprobamos que se han cargado los datos correctamente
docker exec -it hiveserver2 bash
ls -lh /opt/hive/data/warehouse/entrega1.db/info_household/





# row format delimited fields terminated by ',';