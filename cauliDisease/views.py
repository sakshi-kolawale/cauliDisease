import os
import numpy as np
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import UploadedImage

import requests
import io
import gdown

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Load ML model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_model', 'cauliflower_model.h5')
# model = load_model(MODEL_PATH)


def load_model_from_gdrive(file_id):
    url = f"https://drive.google.com/uc?id={file_id}"
    output_path = os.path.join(settings.BASE_DIR, "temp_model.h5")

    # Only download if not already present
    if not os.path.exists(output_path):
        gdown.download(url, output_path, quiet=False)

    # Load the model
    model = load_model(output_path)
    return model


CLASS_NAMES = [
    'Bacterial Spot',
    'Bacterial soft rot',
    'Healthy',
    'Purpling of Cauliflower Curd',
    'Alternaria brassicae',
    'Black Damage (Pectobacterium Carotovorum)'
]  # Update as needed

def predict_image(image_path):
    """Load an image, preprocess it, and predict its class using the model."""
    
    model = load_model_from_gdrive("1cZOrcejhhGjgPTBGeNdpYj88aDHrehpI")

    image = load_img(image_path, target_size=(224, 224))  
    image_array = img_to_array(image) / 255.0  
    image_array = np.expand_dims(image_array, axis=0)  
    predictions = model.predict(image_array)  
    predicted_class = CLASS_NAMES[np.argmax(predictions)]  
    return predicted_class

def index(request):
    """Handles image upload and triggers the prediction."""
    if request.method == 'POST' and request.FILES.get('image'):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            prediction = predict_image(uploaded_image.image.path)
            uploaded_image.prediction = prediction
            uploaded_image.save()
            return redirect('results', pk=uploaded_image.pk)  # Redirect to results page
    else:
        form = ImageUploadForm()

    return render(request, 'index.html', {'form': form})

def results(request, pk):
    """Displays the uploaded image and its prediction result."""
    uploaded_image = UploadedImage.objects.get(pk=pk)
    return render(request, 'results.html', {'uploaded_image': uploaded_image})
