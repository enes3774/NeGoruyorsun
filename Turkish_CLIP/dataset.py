import pandas as pd
from urllib.request import urlopen
from PIL import Image
import torch
import math
import time
from tqdm import tqdm
import time
from urllib.request import Request, urlopen
import numpy as np
class CLIPDataset(torch.utils.data.Dataset):
    def __init__(self, image_filenames,tokenizer,preprocess):

        self.device= "cuda" if torch.cuda.is_available() else "cpu"
        self.image_filenames = image_filenames
        self.data_csv=pd.read_csv(image_filenames)
        self.real_captions=list(self.data_csv.iloc[:, 6])#asıl istenen metinler
        self.yedek_captions=list(self.data_csv.iloc[:, 5])#verilerin yaklaşık %50 sinde istenen veriler Nan bu yüzden o sayfanın başlığını çekiyoruz. Her wiki sayfasının başlığı var

        self.image_urls=list(self.data_csv.iloc[:,2])#istenen urller
        self.captions=[]
        for i in range(len(self.real_captions)):
            if self.real_captions[i]!=self.real_captions[i]:#nan değeri için true
                self.captions.append(self.yedek_captions[i])
            else:
                self.captions.append(self.real_captions[i])
        
        del self.real_captions , self.yedek_captions
     
        self.tokenizer=tokenizer
        self.preprocess = preprocess
        self.max_seq_len=CFG.max_length#bir cümlenin max uzunluğu


    def pad_tokens(self, tokens):
        
        padding = self.max_seq_len - tokens.shape[0]
        if padding > 0:
            tokens = torch.cat((tokens, torch.zeros(padding, dtype=torch.int64) - 1))
            
        elif padding < 0:
            tokens = tokens[:self.max_seq_len]
            
        mask = tokens.ge(1) #cümlenin sonuna gelince attention mask'ı 0 yapıyorum.
        tokens[~mask] = 0
        mask = mask.float()
        del padding
        return tokens,mask
    def __getitem__(self, idx):
        
            

        # header eklememin nedeni wikipedia'dan aralıksız veri çekince hata vermeye başlaması.
        #çok az bir ihtimal de olsa url hatalı olabilir. Program hata vermesin diye try içinde çalışıyor.
        while 1:

            try:
                image_url=self.data_csv.iloc[:, 2][idx]
                req = Request(image_url)
                req.add_header('User-Agent','CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)')
                img = Image.open(urlopen(req))
                del req, image_url
                break
            except :
                
                idx=np.random.randint(0,250000)
                continue
        #image encoder mdeline verilmesi için resim işleniyor.
        
        image = self.preprocess(img).to(self.device)

        tokenized=self.tokenizer(self.captions[idx])
        tokens,attention_mask=self.pad_tokens(torch.tensor(tokenized["input_ids"]))

        return image,tokens,attention_mask
        #NOT: Modelin eğitim süresinin uzun olmasının en büyük nedeni her bir resmi wikipedia'dan çekip, işleyip modele vermem. Bazı wikipedia fotoğrafları 4096x4096 gibi çok yüksek olabiliyor.
        #Bu sorunu çözmek için fotoğrafları indirip saklayabilirisiniz. Fotoğrafları 224x224 boyutunda sakladığımda toplam 152 GB alan kapladı. Bunu yaptığımda model eğitim süresi 20 saatten 1 saate indi.
        

    def __len__(self):
        return len(self.captions)



