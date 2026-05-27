from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'payment-events',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='payment-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("🚀 Kafka Consumer Started")

for message in consumer:

    print(f"📥 Received Event: {message.value}")
