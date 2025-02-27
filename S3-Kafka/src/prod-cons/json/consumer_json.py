from confluent_kafka import Consumer, KafkaError

# Configuración del consumidor
conf = {
    'bootstrap.servers': 'localhost:9093',
    'group.id': 'mi-grupo',
    'auto.offset.reset': 'earliest'  # Lee desde el inicio si no hay offset guardado
}

# Creación del consumidor
consumer = Consumer(conf)

# Suscribirse al topic 'test-topic'
consumer.subscribe(['json-topic'])

try:
    while True:
        # Polling de mensajes (timeout de 1 segundo)
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Error: {msg.error()}")
                break
        # Mostrar el mensaje recibido
        print(f"Mensaje recibido: {msg.value().decode('utf-8')}")
except KeyboardInterrupt:
    pass
finally:
    # Cerrar el consumidor de forma adecuada
    consumer.close()
