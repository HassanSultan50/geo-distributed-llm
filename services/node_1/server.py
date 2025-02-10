from transformers import GPT2Tokenizer
from models.split_gpt_model import GPTNode1
from kafka_services.kafka_producer import send_to_kafka

model = GPTNode1()
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def process_input(input_text):
    """ Tokenizes input, processes first GPT layers, and sends output to Kafka """
    input_tensor = tokenizer.encode(input_text, return_tensors="pt")
    output = model(input_tensor).detach().numpy().tolist()

    # Send processed output to Kafka
    send_to_kafka({"input": input_text, "processed": output})
    return "Data sent to Kafka"

if __name__ == "__main__":
    text = "The AI revolution is"
    print(f"Processing: {text}")
    process_input(text)
