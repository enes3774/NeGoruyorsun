from utils import AvgMeter ,get_lr
from tqdm import tqdm
import config as CFG
from models import CLIPModel
from transformers import AutoModel, AutoTokenizer
import clip
import torch
from dataset import CLIPDataset
def train_epoch(model, train_loader, optimizer, lr_scheduler):
    loss_meter = AvgMeter()
    tqdm_object = tqdm(train_loader, total=len(train_loader))
    for images,input_ids,attention_mask in tqdm_object:
        device=CFG.device
        batch={
            "image":images.to(device),"input_ids":input_ids.to(device),"attention_mask":attention_mask.to(device)
        }
        
        loss = model(batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        count = batch["image"].size(0)
        loss_meter.update(loss.item(), count)

        tqdm_object.set_postfix(train_loss=loss_meter.avg, lr=get_lr(optimizer))
        del loss,count
    return loss_meter
  
  
  train_loader =  build_loaders(bert_tokenizer,clip_preprocess)


clip_model, clip_preprocess = clip.load(CFG.clip_model_name, device=CFG.device)
bert_tokenizer = AutoTokenizer.from_pretrained(CFG.text_tokenizer)
bert_model = AutoModel.from_pretrained(CFG.text_encoder_model)
model = CLIPModel(image_model=clip_model,text_model=bert_model).to(CFG.device)
params = [
    {"params": model.image_encoder.parameters(), "lr": CFG.image_encoder_lr},
    {"params": model.text_encoder.parameters(), "lr": CFG.text_encoder_lr},
    {"params": model.text_projection.parameters(), "lr": CFG.head_lr, "weight_decay": CFG.weight_decay}
]
dataset = CLIPDataset(CFG.data_path,bert_tokenizer,clip_preprocess)
train_loader = torch.utils.data.DataLoader(
        dataset,
        num_workers=CFG.num_workers,
        batch_size=CFG.batch_size,
        shuffle=True
    )
optimizer = torch.optim.AdamW(params, weight_decay=0.)
lr_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode="min", patience=CFG.patience, factor=CFG.factor
)



for epoch in range(CFG.epochs):
    print(f"Epoch: {epoch + 1}")
    model.train()
    train_loss = train_epoch(model, train_loader, optimizer, lr_scheduler)
    
