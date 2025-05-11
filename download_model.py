import os
import gdown

model_dir = 'model'
model_path = os.path.join(model_dir, 'model.joblib')
# Use the correct direct download link for gdown (not the "view" link)
model_url = 'https://drive.google.com/uc?export=download&id=1Ezi8WW3XarglXXz7PDqZalw4ps8IioAX'

if not os.path.exists(model_dir):
    os.makedirs(model_dir)

if not os.path.exists(model_path):
    print("Downloading model.joblib from Google Drive...")
    gdown.download(model_url, model_path, quiet=False)
    print("Download complete.")
else:
    print("Model already exists. Skipping download.")
