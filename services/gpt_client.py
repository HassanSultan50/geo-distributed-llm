import grpc
import gpt_service_pb2
import gpt_service_pb2_grpc
import torch
from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
input_text = "The AI revolution is"
input_tensor = tokenizer.encode(input_text, return_tensors="pt").flatten().tolist()

channel1 = grpc.insecure_channel('localhost:50051')
stub1 = gpt_service_pb2_grpc.GPTNodeStub(channel1)
response1 = stub1.Process(gpt_service_pb2.GPTRequest(input_tensor=input_tensor))

channel2 = grpc.insecure_channel('localhost:50052')
stub2 = gpt_service_pb2_grpc.GPTNodeStub(channel2)
response2 = stub2.Process(gpt_service_pb2.GPTRequest(input_tensor=response1.output_tensor))

print("Final Output Tensor:", response2.output_tensor)
