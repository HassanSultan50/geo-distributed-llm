from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.gpt_inference

def log_inference(input_text, output_text):
    """ Logs input & final output in MongoDB """
    db.logs.insert_one({"input": input_text, "output": output_text})
    print(f"💾 Logged to MongoDB: {input_text} → {output_text}")
