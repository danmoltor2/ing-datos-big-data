from datetime import datetime, timedelta
import os
from pathlib import Path
import json
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.hooks.base import BaseHook
from airflow.providers.apache.kafka.operators.produce import ProduceToTopicOperator
from airflow.models import Variable
import logging
from hdfs import InsecureClient
import time
from kafka import KafkaConsumer
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
import requests
from airflow.providers.apache.hdfs.hooks.webhdfs import WebHDFSHook
from airflow.providers.apache.hive.hooks.hive import HiveServer2Hook

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración predeterminada del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    "retry_delay": timedelta(minutes=1),
    'start_date': datetime(2025, 3, 29)
}

# Creamos el DAG
dag = DAG(
    'dag_sensor',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

# Definimos rutas y variables
csv_file_path = "/opt/airflow/datasets/home_temperature_and_humidity_smoothed_filled.csv"
parquet_file_path = "/opt/airflow/datasets/home_temperature_and_humidity_smoothed_filled.parquet"
hdfs_path = "/topics/sensores/partition=0"

def convert_csv_to_parquet():
    try:
        df = pd.read_csv(csv_file_path)
        
        # Normalizamos los nombres de las columnas
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Realizamos conversiones de tipos de datos para tstp a datetime
        if 'tstp' in df.columns:
            df['tstp'] = pd.to_datetime(df['tstp'])
            # Convertimos timestamp a formato string ISO
            df['tstp'] = df['tstp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Aseguramos que las columnas numéricas sean float
        numeric_columns = [col for col in df.columns if col != 'tstp']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Guardamos en Parquet con compresión Snappy
        df.to_parquet(parquet_file_path, engine='pyarrow', compression='snappy')
        
    except Exception as e:
        print(f"Error al convertir {csv_file_path}: {e}")
        raise

# 1. Tarea para convertir CSV a Parquet
convert_to_parquet_task = PythonOperator(
    task_id='convert_csv_to_parquet',
    python_callable=convert_csv_to_parquet,
    dag=dag
)

# 2. Función para generar mensajes para Kafka a partir del archivo Parquet
def generate_kafka_messages():
    # Leemos el archivo Parquet
    df = pd.read_parquet(parquet_file_path)
    
    # Convertimos tstp a string para que sea serializable en JSON
    if 'tstp' in df.columns:
        df['tstp'] = df['tstp'].astype(str)
    
    # Convertimos cada registro a formato de mensaje para Kafka (key, value)
    messages = []
    for i, record in enumerate(df.to_dict('records')):
        # Usamos un identificador como clave y el registro como valor
        messages.append((f"sensor_record_{i}", json.dumps(record)))
    
    logger.info(f"Se han generado {len(messages)} mensajes desde el archivo Parquet")

    return messages

# Tarea para enviar datos a Kafka usando el operador integrado de Airflow
parquet_to_kafka_task = ProduceToTopicOperator(
    task_id='parquet_to_kafka',
    topic="sensores",
    kafka_config_id="kafka_default",
    producer_function=generate_kafka_messages,
    dag=dag,
)


# Función para verificar que los mensajes se enviaron correctamente
def verify_kafka_messages():
    consumer = KafkaConsumer(
        'sensores',
        bootstrap_servers = 'kafka:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='test_group',
        consumer_timeout_ms=5000
    )

    count = sum(1 for _ in consumer)
    logger.info(f"Se han consumido {count} mensajes desde Kafka")
    return count

check_messages_task = PythonOperator(
    task_id='check_kafka_messages',
    python_callable=verify_kafka_messages,
    provide_context=True,
    dag=dag
)

# 3. Función para crear sink connector
create_sink_task = BashOperator(
    task_id='create_hdfs_sink_connector_bash',
    bash_command='''
    curl -X POST -H "Content-Type: application/json" --data '{
    "name": "hdfs-sink-connector-sensor", 
    "config": { 
        "connector.class": "io.confluent.connect.hdfs.HdfsSinkConnector", 
        "tasks.max": "1", 
        "topics": "sensores", 
        "hdfs.url": "hdfs://namenode:9000", 
        "flush.size": "120", 
        "hdfs.authentication.kerberos": "false", 
        "format.class": "io.confluent.connect.hdfs.json.JsonFormat", 
        "partitioner.class": "io.confluent.connect.storage.partitioner.DefaultPartitioner", 
        "rotate.interval.ms": "60000", 
        "locale": "en", 
        "timezone": "UTC", 
        "value.converter.schemas.enable": "false" 
    }
    }' http://kafka-connect:8083/connectors
    ''',
    dag=dag
)

# Función para verificar si los datos han sido escritos en HDFS
def check_hdfs_data(**context):
    try:
        # Usamos el WebHDFSHook para interactuar con HDFS
        hdfs_hook = WebHDFSHook(webhdfs_conn_id='hdfs_default')
        hdfs_client = hdfs_hook.get_conn()  # Obtiene la conexión a HDFS

        # Listamos archivos en el directorio con detalles
        file_status = hdfs_client.list(hdfs_path, status=True)  # Devuelve nombre y metadatos

        # Extraemos los nombres de los archivos
        file_list = [file[0] for file in file_status]

        # Filtramos los archivos ocultos o temporales
        data_files = [f for f in file_list if not f.startswith('.') and not f.startswith('_')]

        logger.info(f"Número de archivos en HDFS: {len(data_files)}")

        return bool(data_files)

    except Exception as e:
        logger.warning(f"Error al verificar HDFS: {e}")
        return False

# Tarea para verificar si los datos han sido escritos en HDFS
hdfs_sensor_task = PythonOperator(
    task_id='wait_for_hdfs_files',
    python_callable=check_hdfs_data,
    retries=1,
    dag=dag
)

# 4. Creamos la tabla en Hive
def create_hive_table():
    try:
        hive_hook = HiveServer2Hook(hiveserver2_conn_id="hive_default")
        conn = hive_hook.get_conn()
        cursor = conn.cursor()
        
        cursor.execute(f"""
        CREATE EXTERNAL TABLE IF NOT EXISTS sensores (
            tstp STRING,
            temperature_salon FLOAT,
            humidity_salon FLOAT,
            air_salon FLOAT,
            temperature_chambre FLOAT,
            humidity_chambre FLOAT,
            air_chambre FLOAT,
            temperature_bureau FLOAT,
            humidity_bureau FLOAT,
            air_bureau FLOAT,
            temperature_exterieur FLOAT,
            humidity_exterieur FLOAT,
            air_exterieur FLOAT
        )
        ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
        STORED AS TEXTFILE
        LOCATION 'hdfs://namenode:9000{hdfs_path}'
        """)
        cursor.close()
        conn.close()
        logger.info("Tabla creada correctamente en Hive")
    except Exception as e:
        logger.error(f"Error al crear la tabla en Hive: {e}")
        raise
    
# Definición de tareas en Airflow
create_hive_table_task = PythonOperator(
    task_id="create_hive_table",
    python_callable=create_hive_table,
    dag=dag,
)

# 5. Consulta para obtener la temperatura media por ubicación y día
def query_temp_by_location():
    try:
        hive_hook = HiveServer2Hook(hiveserver2_conn_id="hive_default")
        conn = hive_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DATE(tstp) AS dia,
                   AVG(temperature_salon) AS temp_salon,
                   AVG(temperature_chambre) AS temp_chambre,
                   AVG(temperature_bureau) AS temp_bureau,
                   AVG(temperature_exterieur) AS temp_exterieur
            FROM sensores
            GROUP BY DATE(tstp)
        """)
        
        results = cursor.fetchall()
        print("Resultado de la consulta:")
        print("\n".join(map(str, results)))
        
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error en la consulta de temperatura: {e}")
        raise

temp_by_location_task = PythonOperator(
    task_id="query_temp_by_location",
    python_callable=query_temp_by_location,
    dag=dag,
)

# 6. Consulta para detectar los momentos de peor calidad del aire
def query_worst_air_quality():
    try:
        hive_hook = HiveServer2Hook(hiveserver2_conn_id="hive_default")
        conn = hive_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tstp, air_salon, air_chambre, air_bureau, air_exterieur
            FROM sensores
            ORDER BY GREATEST(COALESCE(air_salon, 0), COALESCE(air_chambre, 0), COALESCE(air_bureau, 0), COALESCE(air_exterieur, 0)) DESC
            LIMIT 10
        """)
        
        results = cursor.fetchall()
        print("Resultado de la consulta:")
        print("\n".join(map(str, results)))
        
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error en la consulta de calidad del aire: {e}")
        raise

air_quality_task = PythonOperator(
    task_id="query_worst_air_quality",
    python_callable=query_worst_air_quality,
    dag=dag,
)

# 7. Consulta para detectar variaciones bruscas de humedad
def query_humidity_variation():
    try:
        hive_hook = HiveServer2Hook(hiveserver2_conn_id="hive_default")
        conn = hive_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("""
           WITH humidity_prev AS (
                SELECT tstp, humidity_salon, humidity_chambre, humidity_bureau, humidity_exterieur,
                    LAG(humidity_salon, 4) OVER (ORDER BY tstp) AS prev_humidity_salon,
                    LAG(humidity_chambre, 4) OVER (ORDER BY tstp) AS prev_humidity_chambre,
                    LAG(humidity_bureau, 4) OVER (ORDER BY tstp) AS prev_humidity_bureau,
                    LAG(humidity_exterieur, 4) OVER (ORDER BY tstp) AS prev_humidity_exterieur
                FROM sensores
            ),

            humidity_changes AS (
                SELECT tstp, humidity_salon, prev_humidity_salon, humidity_chambre, prev_humidity_chambre,
                    humidity_bureau, prev_humidity_bureau,humidity_exterieur, prev_humidity_exterieur,
                    ABS((humidity_salon - prev_humidity_salon) / NULLIF(prev_humidity_salon, 0)) AS change_salon,
                    ABS((humidity_chambre - prev_humidity_chambre) / NULLIF(prev_humidity_chambre, 0)) AS change_chambre,
                    ABS((humidity_bureau - prev_humidity_bureau) / NULLIF(prev_humidity_bureau, 0)) AS change_bureau,
                    ABS((humidity_exterieur - prev_humidity_exterieur) / NULLIF(prev_humidity_exterieur, 0)) AS change_exterieur
                FROM humidity_prev
            )

            SELECT tstp, change_salon, change_chambre, change_bureau,  change_exterieur
            FROM humidity_changes
            WHERE 
                change_salon > 0.1
                OR change_chambre > 0.1
                OR change_bureau > 0.1
                OR change_exterieur > 0.1
            ORDER BY tstp
        """)
        
        results = cursor.fetchall()
        print("Resultado de la consulta:")
        print("\n".join(map(str, results)))
        
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error en la consulta de humedad: {e}")
        raise

humidity_variation_task = PythonOperator(
    task_id="query_humidity_variation",
    python_callable=query_humidity_variation,
    dag=dag,
)

# Definimos el flujo de tareas con sus respectivas dependencias
convert_to_parquet_task >> parquet_to_kafka_task >> check_messages_task >> create_sink_task
create_sink_task >> hdfs_sensor_task >> create_hive_table_task
create_hive_table_task >> temp_by_location_task
create_hive_table_task >> air_quality_task
create_hive_table_task >> humidity_variation_task