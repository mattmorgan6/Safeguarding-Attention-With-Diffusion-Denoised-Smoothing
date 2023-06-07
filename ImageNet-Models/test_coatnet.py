import os
from PIL import Image
import timm
import torch
from urllib.request import urlopen

LOCAL_MODEL_PATH = "./pretrained_coatnet.pt"
local_model_exists = os.path.exists(LOCAL_MODEL_PATH)

img = Image.open('/nfs/stak/users/morgamat/hpc-share/CS_499/CS_499_Term_Project/ImageNet-Models/tempo/ILSVRC2012_val_00000004.JPEG')
img = img.convert('RGB')

print("Downloaded test image", flush=True)


model = None
if local_model_exists:
    print("Using local model", flush=True)
    model = torch.load("pretrained_coatnet.pt")
else:
    print("Fetching remote model", flush=True)
    model = timm.create_model('coatnet_rmlp_2_rw_384.sw_in12k_ft_in1k', pretrained=True)
    torch.save(model, LOCAL_MODEL_PATH)

model = model.eval()

# get model specific transforms (normalization, resize)
data_config = timm.data.resolve_model_data_config(model)
transforms = timm.data.create_transform(**data_config, is_training=False)

print("Running prediction:", flush=True)

input_data = transforms(img).unsqueeze(0)
print("Shape:", input_data.shape)
output = model(input_data)  # unsqueeze single image into batch of 1

top5_probabilities, top5_class_indices = torch.topk(output.softmax(dim=1) * 100, k=5)
print(top5_probabilities)
print("\n\n", flush=True)
print(top5_class_indices)