# Eğer coco dataset kullanıyorsan bu dataset.py kullan
from torch.utils.data import Dataset
from transformers import AutoModel, AutoTokenizer
import clip
import json

from torch.utils.data import Dataset
from transformers import AutoModel, AutoTokenizer
import clip
import json
import os
from PIL import Image

class dataset(Dataset):
    """
    A PyTorch Dataset class to be used in a PyTorch DataLoader to create batches.
    """

    def __init__(self,max_len,tokenizer,preprocess,prefix_length=10):
        """
        :param data_folder: folder where data files are stored
        :param data_name: base name of processed datasets
        :param split: split, one of 'TRAIN', 'VAL', or 'TEST'
        :param transform: image transform pipeline
        """
        self.max_seq_len=max_len
        
        with open('../dataset.json') as f:
              self.data = json.load(f)
       
    
        
        self.prefix_length=prefix_length
        
        self.tokenizer=tokenizer
        self.preprocess=preprocess

        # Total number of datapoints
        self.dataset_size = len(self.data)*5
    def pad_tokens(self, tokens):
        padding = self.max_seq_len - tokens.shape[0]
        if padding > 0:
            tokens = torch.cat((tokens, torch.zeros(padding, dtype=torch.int64) - 1))
            
        elif padding < 0:
            tokens = tokens[:self.max_seq_len]
            
        mask = tokens.ge(0)  # mask is zero where we out of sequence
        tokens[~mask] = 0
        mask = mask.float()
        mask = torch.cat((torch.ones(self.prefix_length), mask), dim=0)  # adding prefix mask
        del padding
        return tokens,mask
    def __getitem__(self, i):
        # Unutma i. veri i. metin ama i/number of captions per image 
        img=Image.open(os.path.join("../images_data/mscoco/mscoco_resized/"+str(self.data[i//5]["file_path"][self.data[i//5]["file_path"].index("images")+7:])))
        image = self.preprocess(img).unsqueeze(0).to("cpu")
        #with torch.no_grad():
        #    image_features = self.clip_model.encode_image(image)
        tokenized=self.tokenizer(self.data[i//5]["captions"][i%5])
        padded_tokens,padded_masks=self.pad_tokens(torch.tensor(tokenized["input_ids"]))
        
        return image,padded_tokens,padded_masks
    def __len__(self):
        return self.dataset_size
