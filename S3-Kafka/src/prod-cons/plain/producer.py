from confluent_kafka import Producer
import time

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

# Envío de 10 mensajes al topic 'test'
for i in range(10):
    mensaje = f"Mensaje {i}"
    producer.produce('test-topic', mensaje.encode('utf-8'), callback=delivery_report)
    producer.poll(0)  # Sirve para activar el callback
    time.sleep(1)

# Esperar a que se entreguen todos los mensajes pendientes
producer.flush()
