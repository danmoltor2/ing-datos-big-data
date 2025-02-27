#!/bin/bash

# Espera a que MySQL esté listo (usando 'mysql')
until mysql -h mysql -u root -proot -e "SELECT 1"; do
  sleep 1
done

# Inicializa el metastore (solo la primera vez o si es necesario)
/opt/hive/bin/schematool -dbType mysql -initSchema || true # Ignora el error si ya está inicializado

# Inicia el metastore en segundo plano
hive --service metastore &

# Inicia HiveServer2 en segundo plano
hive --service hiveserver2 &

# Mantén el contenedor en ejecución (crucial)
tail -f /dev/null