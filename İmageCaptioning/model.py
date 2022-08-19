from transformers import AutoModel, AutoTokenizer,AutoModelWithLMHead
from typing import Tuple, Optional, Union
import torch
from torch import nn
class MLP(nn.Module):

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

    def __init__(self, sizes: Tuple[int, ...], bias=True, act=nn.Tanh):
        super(MLP, self).__init__()
        layers = []
        for i in range(len(sizes) - 1):
            layers.append(nn.Linear(sizes[i], sizes[i + 1], bias=bias))
            if i < len(sizes) - 2:
                layers.append(act())
        self.model = nn.Sequential(*layers)
class ClipCaptionModel(nn.Module):

    def get_dummy_token(self, batch_size: int, device: torch.device) -> torch.Tensor:
        return torch.zeros(batch_size, self.prefix_length, dtype=torch.int64, device=device)

    def forward(self, tokens: torch.Tensor, prefix: torch.Tensor, mask: Optional[torch.Tensor] = None,
                labels: Optional[torch.Tensor] = None):
        embedding_text = self.text_model.transformer.wte(tokens)
        
        prefix_projections = self.clip_project(prefix).view(-1, self.prefix_length, self.text_model_embedding_size)
        embedding_cat = torch.cat((prefix_projections, embedding_text), dim=1)
        if labels is not None:
            dummy_token = self.get_dummy_token(tokens.shape[0], tokens.device)
            labels = torch.cat((dummy_token, tokens), dim=1)
        out = self.text_model(inputs_embeds=embedding_cat, labels=labels, attention_mask=mask)
        return out

    def __init__(self, prefix_length: int, prefix_size: int = 512):
        super(ClipCaptionModel, self).__init__()
        self.prefix_length = prefix_length
        self.text_model = AutoModelWithLMHead.from_pretrained("redrussianarmy/gpt2-turkish-cased")
       
        self.text_model_embedding_size = self.text_model.transformer.wte.weight.shape[1]
       
        self.clip_project = MLP((prefix_size, (self.text_model_embedding_size * prefix_length) // 2,
                                     self.text_model_embedding_size * prefix_length))
        
