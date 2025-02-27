from confluent_kafka import Producer
import time
import json
from datetime import datetime
import random

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

# Lista de ciudades para el ejemplo
ciudades = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao"]

# Envío de 10 mensajes al topic 'test-topic'
for i in range(20):
    # Genera datos: fecha y hora actual, ciudad aleatoria y temperatura aleatoria
    datos = {
        "datetime": datetime.now().isoformat(),
        "city": random.choice(ciudades),
        "temperature": round(random.uniform(10.0, 35.0), 2)
    }
    # Convertir el diccionario a cadena JSON
    mensaje_json = json.dumps(datos)
    
    # Enviar mensaje al topic 'test-topic'
    producer.produce('json-topic', mensaje_json.encode('utf-8'), callback=delivery_report)
    producer.poll(0)  # Activar el callback
    time.sleep(1)

# Esperar a que se entreguen todos los mensajes pendientes
producer.flush()
