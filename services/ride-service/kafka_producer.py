from kafka import KafkaProducer
import json


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)


def publish_payment_requested(ride_id):
    event = {
        "ride_id": ride_id,
        "event": "payment_requested"
    }

    future = producer.send("payment-events", event)
    metadata = future.get(timeout=10)

    print(
        f"📤 Kafka accepted: "
        f"ride_id={ride_id}, "
        f"partition={metadata.partition}, "
        f"offset={metadata.offset}"
    )

    return metadata
