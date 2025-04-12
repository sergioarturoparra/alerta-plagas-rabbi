import pika
import json
import logging
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    filename='registro_mensajes.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Credenciales y conexión
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
channel = connection.channel()

# Declaración del exchange
channel.exchange_declare(exchange='alertas_plagas', exchange_type='fanout', durable=False)

# Crear cola exclusiva y temporal
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Enlace entre la cola y el exchange
channel.queue_bind(exchange='alertas_plagas', queue=queue_name)

print("📥 Esperando mensajes de alertas de plagas...")

# Callback al recibir mensaje
def callback(ch, method, properties, body):
    try:
        mensaje = json.loads(body.decode())
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n🔔 [{timestamp}] Alerta recibida:")
        print(f"   🌿 Plaga: {mensaje.get('nombre_plaga')}")
        print(f"   📝 Descripción: {mensaje.get('descripcion')}")
        print(f"   ✅ Recomendación: {mensaje.get('recomendacion')}")

        # Registrar el mensaje
        logging.info(f"Mensaje recibido: {mensaje}")

        # Confirmación manual (opcional)
        # ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logging.error(f"Error procesando mensaje: {e}")
        print("❌ Error procesando mensaje:", e)

# Consumo automático
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True  # Cambia a False si quieres usar confirmación manual
)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("🛑 Conexión cerrada por el usuario.")
    connection.close()