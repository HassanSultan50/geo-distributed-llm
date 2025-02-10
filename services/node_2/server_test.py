import grpc
from concurrent import futures
import torch
from transformers import GPT2Tokenizer
import gpt_service_pb2
import gpt_service_pb2_grpc
from models.split_gpt_model import GPTNode2
from database_service import log_inference

class GPTNode2Servicer(gpt_service_pb2_grpc.GPTNodeServicer):
    def __init__(self):
        self.model = GPTNode2()
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    def Process(self, request, context):
        input_tensor = torch.tensor(request.input_tensor).view(1, -1)
        output = self.model(input_tensor).detach().numpy().flatten().tolist()
        log_inference(str(input_tensor.tolist()), str(output))
        return gpt_service_pb2.GPTResponse(output_tensor=output)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gpt_service_pb2_grpc.add_GPTNodeServicer_to_server(GPTNode2Servicer(), server)
    server.add_insecure_port('[::]:50052')
    print("Node 2 running on port 50052...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
