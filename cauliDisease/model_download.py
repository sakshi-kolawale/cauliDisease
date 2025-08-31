import gdown

url = "https://drive.google.com/uc?id=1cZOrcejhhGjgPTBGeNdpYj88aDHrehpI"
gdown.download(url, "temp_model.h5", quiet=False)
