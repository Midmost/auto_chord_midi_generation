# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-generation", model="breadlicker45/Musenet-1B4-L94-D1024-rwkv-converted")

import torch
# import xformers
print(torch.__version__)
# print(xformers.__version__)
