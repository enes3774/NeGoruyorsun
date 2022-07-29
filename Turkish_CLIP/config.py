# Tüm ayarlanabilir değişkenler burada tutuluyor.

# datasetin içinde olduğu dosya
data_path ="../input/wiki-turkish/wiki_tr_data.tsv"
batch_size = 24
#dataloader kullanırken paralel şekilde verileri alabilirsiniz. Genelde bunun fazla olması kodun daha hızlı çalışmasını sağlar.
num_workers = 10
head_lr = 1e-3
image_encoder_lr = 1e-4
text_encoder_lr = 1e-5
weight_decay = 1e-3
patience = 1
factor = 0.8
epochs = 2
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
clip_model_name="ViT-B/32"
image_embedding = 512
text_encoder_model = "dbmdz/bert-base-turkish-cased"
text_embedding = 768
text_tokenizer = "dbmdz/bert-base-turkish-cased"
#bir metin alabileceği maksimum kelime sayısı
max_length = 200
image_encoder_trainable=False
text_encoder_trainable=True
text_projection_trainable=True
temperature = 1.0

# image size
size = 224

num_projection_layers = 1
projection_dim = 512 
dropout = 0.1
