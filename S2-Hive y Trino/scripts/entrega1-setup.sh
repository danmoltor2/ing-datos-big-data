#!/bin/bash

DATASETS_DIR="../datasets/E1"
INFO_FILE="informations_households.parquet"
HALFHOURLY_DIR="halfhourly_parquet"

# Copiamos los archivos Parquet a Docker
echo "~ Iniciando la copia de archivos Parquet a Docker..."
docker cp "$DATASETS_DIR/$INFO_FILE" hiveserver2:/tmp/$INFO_FILE > /dev/null
echo "Archivo $INFO_FILE copiado."
docker cp "$DATASETS_DIR/$HALFHOURLY_DIR" hiveserver2:/tmp/$HALFHOURLY_DIR > /dev/null
echo "Carpeta $HALFHOURLY_DIR copiada."

# Creamos archivo SQL temporal para la creación de tablas
cat > hive_setup.sql << EOF
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
EOF

# Copiamos y ejecutamos SQL
docker cp hive_setup.sql hiveserver2:/tmp/hive_setup.sql
echo "~ Creando base de datos y tablas..."
docker exec -i hiveserver2 bash -c "beeline -u jdbc:hive2://localhost:10000 -f /tmp/hive_setup.sql"

# Verificamos los datos
echo "~ Verificando datos cargados..."
docker exec -i hiveserver2 bash -c "
  beeline -u jdbc:hive2://localhost:10000 --outputformat=csv2 --showHeader=true -e \"
    SELECT 'Tabla info_household: ', COUNT(*) FROM entrega1.info_household
    UNION ALL 
    SELECT 'Tabla halfhourly: ', COUNT(*) FROM entrega1.halfhourly;
  \"
"