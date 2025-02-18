#!/bin/bash
echo "Esperando a que MySQL esté listo..."
sleep 20  # Esperamos para asegurarnos de que MySQL está listo

echo "Iniciando Metastore de Hive..."
schematool -initSchema -dbType mysql

# Iniciar metastore en segundo plano
hive --service metastore &

# Esperar unos segundos para asegurarse de que el metastore se inicia correctamente
sleep 5  

# Iniciar HiveServer2 en segundo plano
hive --service hiveserver2 &

# Mantener el contenedor en ejecución
tail -f /dev/null