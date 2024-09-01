# Create your views here.
import logging
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .forms import LoginForm
import cv2
import os





# logger = logging.getLogger(__name__)




# def login_view(request):
#     form = LoginForm(request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')  # Redirect to home page or dashboard
#             else:
#                 form.add_error(None, "Invalid email or password")
#     return render(request, 'login.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

# def login_view(request):
#     if request.method == 'POST':
#         print("Received POST request")
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             print("Form is valid")
#             user = form.get_user()
#             print(f"Authenticated user: {user}")
#             login(request, user)
#             return redirect('home')  # Redirect to home or any other page after login
#         else:
#             print("Form is not valid")
#             print("Form errors:", form.errors)
#     else:
#         print("Received GET request")
#         form = AuthenticationForm()

#     return render(request, 'login.html', {'form': form})


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def loginform(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        print(f"Method: {request.method}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        
        # Use email as the username for authentication
        user = authenticate(request, email=email, password=password)
        print(f"Authenticated User: {email}")
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home or any other page after login
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'signup.html')
    else:
        return render(request, 'login.html')



def webcam_feed(request):
    return render(request, 'webcam_feed.html')

def capture_image(request):
    if request.method == 'POST':
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()

        if ret:
            img_name = f"opencv_frame_{request.POST.get('img_counter', 0)}.png"
            cv2.imwrite(os.path.join('static', 'captures', img_name), frame)
            cam.release()
            return JsonResponse({"status": "success", "image_url": f"/static/captures/{img_name}"})
        
        cam.release()
        return JsonResponse({"status": "failed", "message": "Failed to capture image."})

    return JsonResponse({"status": "failed", "message": "Invalid request method."})
