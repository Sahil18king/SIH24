import logging
# from venv import logger
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.contrib.auth.models import User  # Correct import
from django.contrib import messages
# from django.core.files.storage import default_storage
# from django.conf import settings
import os
# import shutil  # For cleaning up the temporary directory
# import tempfile

# from .models import CapturedPhoto

def dashboard(request):
    return render(request, 'dashboard.html')
def loginform(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Method: {request.method}")
        print(f"Email: {email}")
        print(f"Password: {password}")

        # Authenticate using email
        try:
            user = User.objects.get(email=email)  # Fetch user by email
            print(f"User fetched: {user.username}")
            user = authenticate(request, username=user.username, password=password)  # Authenticate using the username (email)
            print(f"Authenticated User: {user}")
        except User.DoesNotExist:
            user = None
            print("User does not exist")

        if user is not None:
            print("User authenticated successfully")
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
        else:
            print("Invalid email or password")
            messages.error(request, 'Invalid email or password')
            return render(request, 'login.html')
    else:
        print("Request method is not POST")
        return render(request, 'login.html')


def webcam_feed(request):
    return render(request, 'webcam_feed.html')

# def capture_image(request):
#     if request.method == 'POST':
#         try:
#             image = request.FILES.get('image')

#             print(request.POST)
#             print(request.FILES.get('location'))

#             location = request.POST.get('location')
#             latitude = request.POST.get('latitude')
#             longitude = request.POST.get('longitude')
#             user_id = request.POST.get('user')

#             print(f"Received image: {image}")
#             print(f"Location: {location}")
#             print(f"Latitude: {latitude}")
#             print(f"Longitude: {longitude}")
#             print(f"User ID: {user_id}")

#             user = User.objects.get(id=user_id) if user_id else None

#             if image:
#                 print("Processing image...")
#                 captured_photo = CapturedPhoto(
#                     photo=image,
#                     location=location,
#                     latitude=latitude,
#                     longitude=longitude,
#                     user=user
#                 )
#                 captured_photo.save()
#                 print(f"Photo saved with ID: {captured_photo.id}")

#                 image_url = captured_photo.photo.url
#                 return JsonResponse({'status': 'success', 'image_url': image_url})
#             else:
#                 print("No image provided")
#                 return JsonResponse({'status': 'error', 'message': 'No image provided'})

#         except Exception as e:
#             print(f"Error: {e}")
#             return JsonResponse({'status': 'error', 'message': str(e)})
#     else:
#         print("Invalid request method")
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



# from .ml_model import detect_garbage, calculate_cleanliness_and_dirtiness, load_model
# def capture_image(request):
#     if request.method == 'POST':
#         uploaded_file = request.FILES.get('image')
#         if uploaded_file:
#             file_path = default_storage.save(f'temp/{uploaded_file.name}', uploaded_file)
#             full_path = os.path.join(settings.MEDIA_ROOT, file_path)

#             try:
#                 model = load_model()
#                 image = cv2.imread(full_path)
#                 if image is None:
#                     return JsonResponse({'error': 'Image could not be loaded.'}, status=400)

#                 average_cleanliness, average_dirtiness = calculate_cleanliness_and_dirtiness(model, image)

#                 return JsonResponse({
#                     'average_cleanliness': average_cleanliness,
#                     'average_dirtiness': average_dirtiness
#                 })
#             except Exception as e:
#                 logger.error(f"Error during image processing: {e}")
#                 return JsonResponse({'error': 'Error processing image.'}, status=500)
#             finally:
#                 if os.path.exists(full_path):
#                     os.remove(full_path)
#         else:
#             return JsonResponse({'error': 'No image uploaded.'}, status=400)

#     return JsonResponse({'error': 'Invalid request method.'}, status=405)







# from urllib.parse import urljoin

# def capture_image(request):
#     if request.method == 'POST':
#         uploaded_file = request.FILES.get('image')
#         if uploaded_file:
#             try:
#                 # Specify the folder where the image will be saved
#                 folder_path = os.path.join(settings.MEDIA_ROOT, 'captured_images')
                
#                 if not os.path.exists(folder_path):
#                     os.makedirs(folder_path)  # Create the folder if it doesn't exist

#                 # Save the file with a unique name to avoid conflicts
#                 file_name = default_storage.save(os.path.join('captured_images', uploaded_file.name), uploaded_file)
#                 file_path = default_storage.path(file_name)
                
#                 # Load the saved image using OpenCV
#                 image = cv2.imread(file_path)
#                 if image is None:
#                     return JsonResponse({'error': 'Image could not be loaded.'}, status=400)
                
#                 try:
#                     # Load the ML model and calculate cleanliness and dirtiness
#                     model = load_model()  # Ensure your load_model() function is correctly implemented
#                     average_cleanliness, average_dirtiness = calculate_cleanliness_and_dirtiness(model, image)

#                     # Return the image URL instead of the file path
#                     image_url = urljoin(settings.MEDIA_URL, file_name)

#                     return JsonResponse({
#                         'average_cleanliness': average_cleanliness,
#                         'average_dirtiness': average_dirtiness,
#                         'image_url': image_url  # Returning image URL instead of file path
#                     })
#                 except Exception as e:
#                     logging.error(f"Error during image processing: {e}")
#                     return JsonResponse({'error': 'Error processing image.'}, status=500)

#             except Exception as e:
#                 logging.error(f"Error saving the image: {e}")
#                 return JsonResponse({'error': 'Error saving the image.'}, status=500)
#         else:
#             return JsonResponse({'error': 'No image uploaded.'}, status=400)

#     return JsonResponse({'error': 'Invalid request method.'}, status=405)



from PIL import Image
from .forms import UploadImageForm
# import io
from .ml_model import load_model, calculate_cleanliness_and_dirtiness  # Assuming these are defined in ml_model.py


def capture_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        print('Here', request.FILES)
        if form.is_valid():
            print('valid')
            form.save()

            return JsonResponse({
                "message": "Success"
            })
        else:
            print(form.errors)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)