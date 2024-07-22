from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import UploadedImage
from PIL import Image, ImageEnhance
import cv2
import io
import numpy as np
from django.core.files.base import ContentFile

def home(request):
    return redirect('upload_image')

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            return redirect('process_image', pk=uploaded_image.pk)
    else:
        form = ImageUploadForm()
    return render(request, 'image_processor/upload.html', {'form': form})

def process_image(request, pk):
    image_instance = UploadedImage.objects.get(pk=pk)
    image_path = image_instance.image.path

    # Open the image using Pillow
    pil_image = Image.open(image_path)

    # Convert the PIL image to an OpenCV image
    cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Example processing: convert to grayscale using OpenCV
    gray_image_cv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # Convert back to PIL image for saving
    gray_image_pil = Image.fromarray(gray_image_cv)

    # Save the processed image to in-memory file
    buffer = io.BytesIO()
    gray_image_pil.save(buffer, format="JPEG")
    buffer.seek(0)
    processed_image_file = ContentFile(buffer.read(), name=f'processed_{image_instance.image.name}')

    # Replace the original image with the processed image
    image_instance.image.save(f'processed_{image_instance.image.name}', processed_image_file)
    
    context = {
        'original_image': image_instance.image.url,
        'processed_image': image_instance.image.url
    }

    return render(request, 'image_processor/process.html', context)

def process_image(request, image_id):
    # Load image
    pil_image = Image.open('path_to_image')

    # Convert to numpy array
    image_array = np.array(pil_image)
    
    # Example processing: Convert RGB to grayscale
    gray_image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    
    # Convert back to PIL Image
    processed_pil_image = Image.fromarray(gray_image_array)

    # Save processed image to disk (for debugging)
    processed_pil_image.save('path_to_save_processed_image')

    # Or if displaying in Django, save to a BytesIO stream
    buffer = BytesIO()
    processed_pil_image.save(buffer, format="PNG")
    buffer.seek(0)
    return HttpResponse(buffer, content_type="image/png")
