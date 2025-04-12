import pika
import json
from datetime import datetime

# Datos simulados de una alerta de plaga
alerta_plaga = {
    'nombre_plaga': 'Trips',
    'descripcion': 'Pequeños insectos que afectan las hojas del aguacate.',
    'recomendacion': 'Aplicar control biológico con depredadores naturales.',
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'ubicacion': 'Fusagasugá'
}

# Configuración de conexión
credentials = pika.PlainCredentials('guest', 'guest')  # ⚠️ Cambiar si usas usuario personalizado
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
channel = connection.channel()

# Declaración del exchange (debe coincidir con el suscriptor)
channel.exchange_declare(exchange='alertas_plagas', exchange_type='fanout', durable=False)

# Publicación del mensaje
channel.basic_publish(
    exchange='alertas_plagas',
    routing_key='',
    body=json.dumps(alerta_plaga)
)

print("📤 Alerta enviada correctamente:")
print(json.dumps(alerta_plaga, indent=2))

# Cierre de conexión
connection.close()