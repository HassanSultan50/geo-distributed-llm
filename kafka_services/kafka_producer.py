from kafka import KafkaProducer
import json

KAFKA_BROKER = "localhost:9092"
INFERENCE_TOPIC = "gpt-inference"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka(layer1_output):
    """ Send processed data from Node 1 to Kafka """
    producer.send(INFERENCE_TOPIC, layer1_output)
    producer.flush()
    print(f"📨 Sent to Kafka: {layer1_output}")

# Example Usage:
if __name__ == "__main__":
    send_to_kafka({"input": "Hello AI", "processed": [0.1, 0.2, 0.3]})
