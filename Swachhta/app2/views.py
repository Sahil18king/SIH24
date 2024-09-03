import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.contrib.auth.models import User  # Correct import
from django.contrib import messages

from .models import CapturedPhoto
import cv2
import os

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
#         image = request.FILES.get('image')
#         location = request.POST.get('location')
#         latitude = request.POST.get('latitude')
#         longitude = request.POST.get('longitude')
#         user_id = request.POST.get('user')

#         print(f"Received image: {image}")
#         print(f"Location: {location}")
#         print(f"Latitude: {latitude}")
#         print(f"Longitude: {longitude}")
#         print(f"User ID: {user_id}")

#         user = User.objects.get(id=user_id) if user_id else None

#         if image:
#             print("Processing image...")
#             captured_photo = CapturedPhoto(
#                 photo=image,
#                 location=location,
#                 latitude=latitude,
#                 longitude=longitude,
#                 user=user
#             )
#             captured_photo.save()
#             print(f"Photo saved with ID: {captured_photo.id}")

#             image_url = captured_photo.photo.url
#             return JsonResponse({'status': 'success', 'image_url': image_url})

#         print("No image provided")
#         return JsonResponse({'status': 'error', 'message': 'No image provided'})
    
#     print("Invalid request method")
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def capture_image(request):
    if request.method == 'POST':
        try:
            image = request.FILES.get('image')
            location = request.POST.get('location')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            user_id = request.POST.get('user')

            print(f"Received image: {image}")
            print(f"Location: {location}")
            print(f"Latitude: {latitude}")
            print(f"Longitude: {longitude}")
            print(f"User ID: {user_id}")

            user = User.objects.get(id=user_id) if user_id else None

            if image:
                print("Processing image...")
                captured_photo = CapturedPhoto(
                    photo=image,
                    location=location,
                    latitude=latitude,
                    longitude=longitude,
                    user=user
                )
                captured_photo.save()
                print(f"Photo saved with ID: {captured_photo.id}")

                image_url = captured_photo.photo.url
                return JsonResponse({'status': 'success', 'image_url': image_url})
            else:
                print("No image provided")
                return JsonResponse({'status': 'error', 'message': 'No image provided'})

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        print("Invalid request method")
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
