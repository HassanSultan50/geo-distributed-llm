from kafka import KafkaConsumer
import json
from services.database_service import log_inference
from models.split_gpt_model import GPTNode2
import torch

KAFKA_BROKER = "localhost:9092"
INFERENCE_TOPIC = "gpt-inference"

consumer = KafkaConsumer(
    INFERENCE_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

model = GPTNode2()

def process_kafka_message():
    """ Listens for messages, processes final GPT-2 layers, and stores result in MongoDB """
    for message in consumer:
        layer1_output = message.value["processed"]
        print(f"📥 Received from Kafka: {layer1_output}")

        # Convert received tensor back to PyTorch format
        input_tensor = torch.tensor(layer1_output).view(1, -1)

        # Process final GPT layers (Node 2)
        output = model(input_tensor).detach().numpy().tolist()

        # Log to MongoDB
        log_inference(message.value["input"], output)
        print(f"✅ Final GPT-2 Output: {output}")

# Example Usage:
if __name__ == "__main__":
    process_kafka_message()
