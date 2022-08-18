from pytube import YouTube
import cv2
from PIL import Image
from model import ClipCaptionModel
import clip
import skimage.io as io
from utils import generate2,generate_beam
from torchvision import transforms
import torch
prefix_length=10
prefix_dim=512

ai_model = ClipCaptionModel(prefix_length, prefix_size=prefix_dim)
ai_model.load_state_dict(torch.load("checkpoints/model_latest.pt"))
device= torch.device("cuda" if torch.cuda.is_available() else "cpu")
ai_model=ai_model.to(device)
clip_model,clip_preprocessor=clip.load("ViT-B/32", device=device)
N = 120

video_url = "https://www.youtube.com/watch?v=wkHqkDK3SJg&t=62s"  
streams = YouTube(video_url).streams.filter(adaptive=True, subtype="mp4", resolution="360p", only_video=True)

if len(streams) == 0:
    raise "uygun stream bulunamadı."


streams[0].download(filename="video.mp4")
print("yüklendi")



video_frames = []

capture = cv2.VideoCapture('video.mp4')
fps = capture.get(cv2.CAP_PROP_FPS)

current_frame = 0
while capture.isOpened():

    ret, frame = capture.read()


    if ret == True:
        video_frames.append(Image.fromarray(frame[:, :, ::-1]))
    else:
        break


    current_frame += N
    capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame)

print(f"Çıkartılan frame saysı: {len(video_frames)}")


def image_to_text(pil_image):
    image = clip_preprocessor(pil_image).unsqueeze(0).to(device)
    with torch.no_grad():
   
        prefix = clip_model.encode_image(image).to(device, dtype=torch.float32)
    
        prefix_embed = ai_model.clip_project(prefix).reshape(1, prefix_length, -1)

    generated_text_prefix = generate_beam(ai_model, AutoTokenizer.from_pretrained("redrussianarmy/gpt2-turkish-cased"), embed=prefix_embed)[0]
    return generated_text_prefix
texts=[]
for i in range(len(video_frames)):
    text=image_to_text(video_frames[i])
    texts.append(text)
print(texts)
