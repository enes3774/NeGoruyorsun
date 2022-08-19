from model import ClipCaptionModel
import PIL
import clip
import skimage.io as io
from utils import generate2,generate_beam
import torch
from torchvision import transforms
prefix_length=10
prefix_dim=512

ai_model = ClipCaptionModel(prefix_length, prefix_size=prefix_dim)
ai_model.load_state_dict(torch.load("checkpoints/model_latest.pt"))
device= torch.device("cuda" if torch.cuda.is_available() else "cpu")
ai_model=ai_model.to(device)
clip_model,clip_preprocessor=clip.load("ViT-B/32", device=device)
use_beam_search = True
UPLOADED_FILE="test.jpg"
image = io.imread(UPLOADED_FILE)

pil_image = PIL.Image.fromarray(image)

image = clip_preprocessor(pil_image).unsqueeze(0).to(device)
with torch.no_grad():
    prefix = clip_model.encode_image(image).to(device, dtype=torch.float32)
    prefix_embed = ai_model.clip_project(prefix).reshape(1, prefix_length, -1)
if use_beam_search:
    generated_text_prefix = generate_beam(ai_model, AutoTokenizer.from_pretrained("redrussianarmy/gpt2-turkish-cased"), embed=prefix_embed)[0]
else:
    generated_text_prefix = generate2(ai_model, AutoTokenizer.from_pretrained("redrussianarmy/gpt2-turkish-cased"), embed=prefix_embed)


print('\n')
print(generated_text_prefix)
