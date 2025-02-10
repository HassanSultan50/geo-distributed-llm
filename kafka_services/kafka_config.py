from kafka import KafkaProducer, KafkaConsumer

KAFKA_BROKER = "kafka:9092"
INFERENCE_TOPIC = "gpt-inference"

def get_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: str(v).encode('utf-8')
    )

def get_kafka_consumer():
    return KafkaConsumer(
        INFERENCE_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="earliest",
        value_deserializer=lambda v: v.decode('utf-8')
    )
