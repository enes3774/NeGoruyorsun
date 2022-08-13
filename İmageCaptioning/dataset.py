
from torch.utils.data import Dataset
from transformers import AutoModel, AutoTokenizer
import clip
import json

class dataset(Dataset):
   
   

    def __init__(self,max_len,tokenizer,preprocess,prefix_length=10):
        """
        :param max_len: alınan metinler en çok kaç uzunluğunda olsun
        :param tokenizer: metileri tokenleştirmek için tokenizer
        :param preprocess: clip modele resimler verilmesi için ön hazırlık
        :param prefix_length: gpt modeline verilecek embeddingleşmiş kelime uzunluğu
        """
        self.max_seq_len=max_len
        
        dataset=json.load(open("../input/flickrturkishdataset/tasviret8k_captions.json"))#içinde resim dosyalarını ve metinleri bulundurmalı
        dataset=dataset["images"]
        self.captions=[]
        self.image_names=[]
        for i in range(len(dataset)):
            for j in range(len(dataset[i]["sentids"])):
                self.captions.append(dataset[i]["sentences"][j]["raw"])
                self.image_names.append(dataset[i]["filename"][:dataset[i]["filename"].find("_")])
        
        
        
        self.prefix_length=prefix_length
        
        self.tokenizer=tokenizer
        self.preprocess=preprocess

        # toplam veri sayısı
        self.dataset_size = len(self.captions)
    def pad_tokens(self, tokens):
        
        padding = self.max_seq_len - tokens.shape[0]
        if padding > 0:
            tokens = torch.cat((tokens, torch.zeros(padding, dtype=torch.int64) - 1))
            
        elif padding < 0:
            tokens = tokens[:self.max_seq_len]
            
        mask = tokens.ge(0) 
        tokens[~mask] = 0
        mask = mask.float()
        mask = torch.cat((torch.ones(self.prefix_length), mask), dim=0)  
        del padding
        return tokens,mask
    def __getitem__(self, i):
        # Unutma i. veri i. metin ama bazı resimler birden fazla metni var
        img=Image.open(f"../input/flickr-image-dataset/flickr30k_images/flickr30k_images/{self.image_names[i]}.jpg")
        image = self.preprocess(img).unsqueeze(0).to("cpu") # paralel workerslar çalıştırmak için cpu gerekli
        
        tokenized=self.tokenizer(self.captions[i])
        padded_tokens,padded_masks=self.pad_tokens(torch.tensor(tokenized["input_ids"]))
        
        return image,padded_tokens,padded_masks
    def __len__(self):
        return len(self.captions)-1
