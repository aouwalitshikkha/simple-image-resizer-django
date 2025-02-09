from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image
from io import BytesIO
from .forms import ImageResizeForm
import os

def upload_image_file(request):
    """Handles the image upload for Dropzone.js"""
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']

        # Save the file inside the media directory (e.g., media/temp_images/)
        file_name = os.path.join('temp_images', file.name)
        file_path = default_storage.save(file_name, ContentFile(file.read()))
        file_path = default_storage.path(file_path)
        file_url = settings.MEDIA_URL + file_path

        return JsonResponse({'image_path': file_url})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def upload_and_resize_image(request):
    """Displays the form and handles image resizing"""
    if request.method == 'POST':
        # Process the form and image resizing
        form = ImageResizeForm(request.POST)
        if form.is_valid():
            image_path = request.POST.get('uploaded_image_path')
            if not image_path:
                return HttpResponse('No valid image uploaded', status=400)
            image_path = image_path.replace(settings.MEDIA_URL, '', 1)
            if not default_storage.exists(image_path):
                return HttpResponse('No valid image uploaded', status=400)

            # Resize logic
            width = form.cleaned_data.get('width') or 1920  # Default to 1920 if not provided
            height = form.cleaned_data.get('height') or 1080  # Default to 1080 if not provided
            maintain_aspect_ratio = form.cleaned_data.get('maintain_aspect_ratio')
            output_format = form.cleaned_data.get('output_format')
            quality = form.cleaned_data.get('quality')

            with default_storage.open(image_path) as image_file:
                img = Image.open(BytesIO(image_file.read()))

            if maintain_aspect_ratio:
                original_width, original_height = img.size
                if width:
                    height = int((width / original_width) * original_height)
                elif height:
                    width = int((height / original_height) * original_width)

            img = img.resize((width, height), Image.LANCZOS)

            # Save and return the resized image
            buffer = BytesIO()
            img.save(buffer, format=output_format.upper(), quality=quality)
            buffer.seek(0)
            response = HttpResponse(buffer, content_type=f'image/{output_format}')
            response['Content-Disposition'] = f'attachment; filename="resized_image.{output_format}"'

            # Delete the temporary image file after sending the response
            default_storage.delete(image_path)

            return response
    else:
        # Display the form for GET requests
        form = ImageResizeForm()

    return render(request, 'upload_image.html', {'form': form})
