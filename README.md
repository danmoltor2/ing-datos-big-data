# Hadoop Cluster con Docker Compose  

Este repositorio contiene los archivos necesarios para desplegar un clúster de **Hadoop** utilizando **Docker Compose**. La configuración incluye los principales componentes de Hadoop, como **HDFS (Namenode y Datanodes)** y los servicios esenciales para su funcionamiento.  

## 🚀 Características  

- Configuración automatizada de un clúster Hadoop en contenedores.  
- Implementación de **HDFS** con **Namenode** y dos **Datanodes**.  
- Uso de **Docker Compose** para una gestión sencilla de los servicios.  
- Configuración optimizada para pruebas y desarrollo.  

## 📂 Estructura del Repositorio  

```
📁 hadoop-cluster-docker
│── 📄 docker-compose.yml        # Definición de los servicios Hadoop en Docker
│── 📂 hadoop-config             # Configuraciones de Hadoop (core-site.xml, hdfs-site.xml, etc.)
│── 📂 scripts                   # Scripts de inicialización y configuración
│── 📂 src                       # Código de proyectos de las sesiones
│── 📂 datasets                  # Pues eso, los datos que se usan en los proyectos
│── 📄 README.md                 # Este documento
```

## 🛠️ Requisitos  

- **Docker** y **Docker Compose** instalados en el sistema.  
- Al menos **4 GB de RAM** para ejecutar múltiples contenedores.  

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

## 📝 Notas  

- El sistema está configurado para un entorno de desarrollo, no para producción.  
- Se pueden añadir más **Datanodes** editando el `docker-compose.yml`.  

## 📖 Referencias  

- [Documentación oficial de Hadoop](https://hadoop.apache.org/docs/stable/)  
- [Docker Hub - Hadoop Images](https://hub.docker.com/)  