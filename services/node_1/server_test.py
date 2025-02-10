import grpc
from concurrent import futures
import torch
from transformers import GPT2Tokenizer
import gpt_service_pb2
import gpt_service_pb2_grpc
from models.split_gpt_model import GPTNode1

class GPTNode1Servicer(gpt_service_pb2_grpc.GPTNodeServicer):
    def __init__(self):
        self.model = GPTNode1()
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    def Process(self, request, context):
        input_tensor = torch.tensor(request.input_tensor).view(1, -1)
        output = self.model(input_tensor).detach().numpy().flatten().tolist()
        return gpt_service_pb2.GPTResponse(output_tensor=output)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gpt_service_pb2_grpc.add_GPTNodeServicer_to_server(GPTNode1Servicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Node 1 running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
