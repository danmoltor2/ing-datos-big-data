<a name="readme-top"></a>
# Ingeniería de Datos: Big Data

Este repositorio contiene los diferentes entornos de desarrollo que se utilizan para la asignatura **Ingeniería de Datos: Big Data** del **Máster en Ingeniería del Software - Cloud, Datos y Gestión TI** de la Escuela Técnica Superior de Ingeniería Informática de la Universidad de Sevilla.

## 🚀 Características  

- 📌 Entorno basado en Docker: Fácil despliegue y configuración de los servicios.

- 📁 Soporte para Hadoop: Ejecución de trabajos de MapReduce con ejemplos prácticos.

- 🔍 Hive y Trino: Consultas SQL sobre datos distribuidos en HDFS.

- 📡 Kafka: Procesamiento en tiempo real con productores y consumidores.

- 🚀 Apache Airflow: Orquestación de flujos de datos con DAGs personalizados.

- 📊 Incluye datasets de prueba: Archivos de texto y CSV para experimentación.

- 🔄 Modularidad: Separación clara de los entornos en sesiones específicas. 


## 📂 Estructura del Repositorio  

```
📂 Proyecto
├── 📂 datasets/                     # Conjunto de datos utilizados en el proyecto
│   ├── 📂 E0/
│   ├── 📂 E1/
│   ├── 📂 E2/
│   ├── 📄 quijote.txt
│   ├── 📄 README.txt
│
├── 📂 S1-hadoop/                    # Configuración y scripts para Hadoop (Sesión 1)
│   ├── 📄 docker-compose.yml
│   ├── 📄 dockerfile
│   ├── 📂 hadoop_config/
│   ├── 📂 scripts/
│   ├── 📂 src/MapReduce/
│
├── 📂 S2-Hive y Trino/              # Configuración de Hive y Trino (Sesión 2)
│   ├── 📄 docker-compose.yml
│   ├── 📄 dockerfile
│   ├── 📂 hadoop_config/
│   ├── 📂 hive/
│   ├── 📂 trino-config/
│   ├── 📂 scripts/
│   ├── 📂 src/MapReduce/
│
├── 📂 S3-Kafka/                     # Configuración de Kafka y productores/consumidores (Sesión 3)
│   ├── 📄 docker-compose.yml
│   ├── 📄 dockerfile
│   ├── 📂 hadoop_config/
│   ├── 📂 scripts/
│   ├── 📂 src/prod-cons/
│
├── 📂 S4-Airflow/                   # Configuración de Apache Airflow (Sesión 4)
│   ├── 📄 docker-compose.yml
│   ├── 📄 Dockerfile.airflow
│   ├── 📂 hadoop_config/
│   ├── 📂 scripts/
│   ├── 📂 src/
│
├── 📄 .gitignore                    # Archivos y carpetas ignorados por Git
├── 📄 README.md                      # Documentación del repositorio
```

## 🛠️ Requisitos  

- **Docker** y **Docker Compose** instalados en el sistema.  
- **RAM**: Mínimo 8GB (recomendado 16GB+ para entornos completos).
- **Espacio en disco**: Al menos 20GB libres para contenedores y datos.

## ⚡ Instalación y Uso  

1️⃣ Clona este repositorio:  
```sh
git clone https://github.com/josemarialuna/hdfs-docker-cluster.git
cd hdfs-docker-cluster
```

2️⃣ Inicia el clúster de Hadoop con Docker Compose:  
```sh
docker-compose up -d
```

3️⃣ Verifica que los contenedores están en ejecución:  
```sh
docker ps
```

4️⃣ Accede al **Namenode** para interactuar con HDFS:  
```sh
docker exec -it namenode bash
```
<p align="right">(<a href="#readme-top">Volver arriba</a>)</p>

## 📌 Comandos Útiles  

🔹 Listar los archivos en HDFS:  
```sh
hdfs dfs -ls /
```

🔹 Subir un archivo a HDFS:  
```sh
hdfs dfs -put archivo.txt /ruta/destino/
```

🔹 Descargar un archivo de HDFS:  
```sh
hdfs dfs -get /ruta/origen/archivo.txt .
```

🔹 Ver el estado del clúster:  
```sh
hdfs dfsadmin -report
```

🔹 Salir manualmente del Safe Mode: 
```sh
hdfs dfsadmin -safemode leave
```

🔹 Verificar replicación de bloques y balancear datos:
```sh
hdfs fsck /
hdfs balancer
```



<p align="right">(<a href="#readme-top">Volver arriba</a>)</p>


## 📝 Notas  

- El sistema está configurado para un entorno de desarrollo, no para producción.  
- Se pueden añadir más **Datanodes** editando el `docker-compose.yml`.  

##  FAQ  
**El namenode me da un error de unexpected end of file**
Verifica caracteres ocultos en el fichero. Ejecuta:
```sh
cat -A start-hdfs.sh
```
Si ves ^M al final de las líneas, el archivo tiene formato Windows y debes convertirlo.
```sh
sed -i 's/\r$//' start-hdfs.sh
```


## 📖 Referencias  

- [Documentación oficial de Hadoop](https://hadoop.apache.org/docs/stable/)  
- [Docker Hub - Hadoop Images](https://hub.docker.com/)  

<p align="right">(<a href="#readme-top">Volver arriba</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/josemarialuna/hdfs-docker-cluster.svg?style=for-the-badge
[contributors-url]: https://github.com/josemarialuna/hdfs-docker-cluster/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/josemarialuna/hdfs-docker-cluster.svg?style=for-the-badge
[forks-url]: https://github.com/josemarialuna/hdfs-docker-cluster/network/members
[stars-shield]: https://img.shields.io/github/stars/josemarialuna/hdfs-docker-cluster.svg?style=for-the-badge
[stars-url]: https://github.com/josemarialuna/hdfs-docker-cluster/stargazers
[issues-shield]: https://img.shields.io/github/issues/josemarialuna/hdfs-docker-cluster.svg?style=for-the-badge
[issues-url]: https://github.com/josemarialuna/hdfs-docker-cluster/issues
[license-shield]: https://img.shields.io/github/license/josemarialuna/hdfs-docker-cluster.svg?style=for-the-badge
[license-url]: https://github.com/josemarialuna/hdfs-docker-cluster/blob/master/LICENSE.txt
[personal-shield]: https://img.shields.io/badge/Personal%20Site-555?style=for-the-badge
[personal-url]: https://josemarialuna.com