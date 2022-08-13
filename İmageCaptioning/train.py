
import time
from models import ClipCaptionModel
from dataset import dataset
import clip
from PIL import Image
from utils import AvgMeter,get_lr
import os
clip_model_name="ViT-B/32"
text_tokenizer = "redrussianarmy/gpt2-turkish-cased"
device= torch.device("cuda" if torch.cuda.is_available() else "cpu")
clip_model, clip_preprocess = clip.load(clip_model_name, device=device)
bert_tokenizer = AutoTokenizer.from_pretrained(text_tokenizer)
dataset=dataset(50,bert_tokenizer,clip_preprocess)

lr= 2e-5
warmup_steps= 5000
#model kayıt klasoru ve kaydedilecek ön isim
output_dir="checkpoints"
output_prefix = "model"


batch_size = 32
epochs = 10
print("total epoch:"+str(epochs))
if not os.path.exists(output_dir):
     os.makedirs(output_dir)
prefix_length=10
prefix_dim=512

ai_model = ClipCaptionModel(prefix_length, prefix_size=prefix_dim)
ai_model = ai_model.to(device)
ai_model.train()
optimizer = AdamW(ai_model.parameters(), lr=lr)
train_dataloader = DataLoader(dataset,num_workers=8 ,batch_size=batch_size,shuffle=True, drop_last=True)
scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=warmup_steps, num_training_steps=epochs * len(train_dataloader)
    )
start=time.time()
for epoch in range(epochs):
        print(f">>> Training epoch {epoch}")
        sys.stdout.flush()
        #daha iyi bir gözlem için ortalama loss yazdırılacak
        loss_meter = AvgMeter()
        
        for idx, (images,tokens, mask) in enumerate(train_dataloader):
            images=images.squeeze()
            #model, clip embeddingsleri alıp metne çevirecek 
            with torch.no_grad():
                prefix=clip_model.encode_image(images.to(device))
            ai_model.zero_grad()
            tokens, mask, prefix = tokens.to(device), mask.to(device), prefix.to(device, dtype=torch.float32)
            outputs = ai_model(tokens, prefix, mask)
            logits = outputs.logits[:, prefix_length - 1: -1]
            loss = nnf.cross_entropy(logits.reshape(-1, logits.shape[-1]), tokens.flatten(), ignore_index=0)
            loss.backward()
            optimizer.step()
            
            loss_meter.update(loss.item(), batch_size)
            scheduler.step()
            optimizer.zero_grad()
           
            #her 6000 adımda bir model kaydedilecek
            if (idx) % 6000 == 0:
                torch.save(
                    ai_model.state_dict(),
                    os.path.join(output_dir, f"{output_prefix}_{idx}_latest.pt"),
                )
             #400 adımda bir model sonuçları yazdırılır.
            if idx%400==0:
                end=time.time()
                print(f"idx:{idx} avg loss:{loss_meter.avg} time:{end-start} lr:{get_lr(optimizer)} loss:{loss.item()}")
                start=time.time()
       
    
        torch.save(
                    ai_model.state_dict(),
                    os.path.join(output_dir, f"epoch_{epoch}_{output_prefix}_latest.pt"),
                )
    
