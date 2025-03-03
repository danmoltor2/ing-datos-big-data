<a name="readme-top"></a>
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