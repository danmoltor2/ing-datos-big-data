import csv
import json
import time
from datetime import datetime
from confluent_kafka import Producer
# import os

# print(os.getcwd())

# Función para el callback de entrega de mensajes
def delivery_report(err, msg):
    if err is not None:
        print(f"Error en la entrega: {err}")
    else:
        print(f"Mensaje entregado a {msg.topic()} [{msg.partition()}]: {msg.value().decode('utf-8')}")

# Configuración del productor
conf = {'bootstrap.servers': 'localhost:9093'}

# Creación del productor
producer = Producer(conf)

# Leer datos del CSV y enviarlos a Kafka
with open("./data/amazon.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Convertir cada fila a formato JSON
        amazon = {
            "datetime": datetime.now().isoformat(),
            "data": row  # Se envía toda la fila del CSV como JSON
        }
        mensaje_json = json.dumps(amazon)

        # Enviar mensaje al topic 'json-topic'
        producer.produce('transactions', mensaje_json.encode('utf-8'), callback=delivery_report)
        producer.poll(0)  # Activar el callback
        # time.sleep(1)

# Esperar a que se entreguen todos los mensajes pendientes
producer.flush()

# Para ejecutar el sink de Kafka:
# curl -X POST -H "Content-Type: application/json" --data @src/prod-cons/json/hdfs-sink-config.json http://localhost:8083/connectors