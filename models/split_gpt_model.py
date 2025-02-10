from transformers import GPT2Model
import torch.nn as nn

class GPTNode1(nn.Module):
    """ First 6 layers of GPT-2 """
    def __init__(self):
        super(GPTNode1, self).__init__()
        self.model = GPT2Model.from_pretrained("gpt2")
        self.layers = self.model.h[:6]  

    def forward(self, x):
        return self.layers(x.last_hidden_state)


class GPTNode2(nn.Module):
    """ Final 6 layers + output processing """
    def __init__(self):
        super(GPTNode2, self).__init__()
        self.model = GPT2Model.from_pretrained("gpt2")
        self.layers = self.model.h[6:]  
        self.ln_f = self.model.ln_f

    def forward(self, x):
        return self.ln_f(self.layers(x))
