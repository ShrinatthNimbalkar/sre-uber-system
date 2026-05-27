from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("🚀 Kafka Producer Started")

while True:

    event = {
        "ride_id": 101,
        "event": "payment_requested"
    }

    producer.send("payment-events", event)

    print(f"📤 Sent Event: {event}")

    time.sleep(5)
