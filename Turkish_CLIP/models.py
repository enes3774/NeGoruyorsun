import os

import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

import torch
from torch import nn

import config as CFG

class ProjectionHead(nn.Module):
    def __init__(
        self,
        embedding_dim,
        projection_dim=CFG.projection_dim,
        dropout=CFG.dropout
    ):
         
        
        super().__init__()
       
        self.projection = nn.Linear(embedding_dim, projection_dim)
        self.gelu = nn.GELU()
        self.fc = nn.Linear(projection_dim, projection_dim)
        self.dropout = nn.Dropout(dropout)
        self.layer_norm = nn.LayerNorm(projection_dim)
    
    def forward(self, x):
        projected = self.projection(x)
        x = self.gelu(projected)
        x = self.fc(x)
        x = self.dropout(x)
        x = x + projected
        x = self.layer_norm(x)
        return x


class TextEncoder(nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model=model
            
        for p in self.model.parameters():
            p.requires_grad = True

       
        self.target_token_idx = 0

    def forward(self, input_ids, attention_mask):
        output = self.model(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_state = output.last_hidden_state
        return last_hidden_state[:, self.target_token_idx, :]

class CLIPModel(nn.Module):
    def __init__(
        self,
        image_model,
        text_model,
        temperature=CFG.temperature,
        image_embedding=CFG.image_embedding,
        text_embedding=CFG.text_embedding
        
    ):
        """
        modeller dahil ediliyor. 3 tane model var: image encoder,text encoder ve text projection. Text encoder ve image encoder outut vektörleri farklı olduğu için 
        text encoder sonucunda çıkan vektörü image encoder ile uyumlu yapmak için bir projection head kullanıyorum.
        Eğer daha iyi bir model isterseniz önce sadece projection headı birkaç adım eğitin sonrasında text encoder ile birlikte eğitebilirsiniz.
        
        
        """
        super().__init__()
        self.image_encoder = image_model.to(CFG.device)
        for p in self.image_encoder.parameters():
            p.requires_grad = CFG.image_encoder_trainable
        self.text_encoder = TextEncoder(text_model).to(CFG.device)
      
        #self.image_projection = ProjectionHead(embedding_dim=image_embedding)
        self.text_projection = ProjectionHead(embedding_dim=text_embedding).to(CFG.device)
        for p in self.text_projection.parameters():
            p.requires_grad = CFG.text_projection_trainable
        self.temperature = temperature

    def forward(self, batch):
        image_embeddings = self.image_encoder.encode_image(batch["image"]).float()
        text_features = self.text_encoder(
            input_ids=batch["input_ids"], attention_mask=batch["attention_mask"]
        )
        
        
   
        text_embeddings = self.text_projection(text_features)

        # loss hesaplanması
        logits = (text_embeddings @ image_embeddings.T) / self.temperature
        images_similarity = image_embeddings @ image_embeddings.T
        texts_similarity = text_embeddings @ text_embeddings.T
        targets = F.softmax(
            (images_similarity + texts_similarity) / 2 * self.temperature, dim=-1
        )
        texts_loss = cross_entropy(logits, targets, reduction='none')
        images_loss = cross_entropy(logits.T, targets.T, reduction='none')
        loss =  (images_loss + texts_loss) / 2.0 
        return loss.mean()


def cross_entropy(preds, targets, reduction='none'):
    log_softmax = nn.LogSoftmax(dim=-1)
    loss = (-targets * log_softmax(preds)).sum(1)
    if reduction == "none":
        return loss
    elif reduction == "mean":
        return loss.mean()
