import time

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .models import User


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
@csrf_exempt
def login_view(request):

    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            context = {'user': user}
            return render(request, 'homeProfile.html', context)
        else:
            return HttpResponseBadRequest('Login Failed')


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def sign_up(request):
    if request.method == 'GET':
        return render(request, 'signup.html')

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            return HttpResponseBadRequest('Email already exists. Please choose a different Email.')

        if User.objects.filter(username=username).exists():
            return HttpResponseBadRequest('Username already exists. Please choose a different Username.')
        User.objects.create_user(email=email, username=username, password=password)
        return render(request, 'login.html')


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def update_user(request):
    print(request)
    print("User in update_user:", request.user)

    if request.method == 'GET':
        user = request.user
        return render(request, 'homeProfile.html', {'user': user})

    if request.method == 'POST':
        user = request.user
        print("Hello")

        # Check if the user is authenticated
        if user.is_authenticated:
            print("User is authenticated!")
            location = request.POST.get("location")
            bio = request.POST.get("bio")
            quote = request.POST.get("quote")
            user.bio = bio
            user.location = location
            user.quote = quote
            user.save()
            user_data = {
                'id': user.id,
                'username': user.username,
                'location': user.location,
                'quote': user.quote,
                'bio': user.bio,
            }
            return JsonResponse({'success': True, 'user': user_data})
        else:
            print("User not authenticated!")
            return JsonResponse({'success': False, 'error': 'User not authenticated'}, status=401)

@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def neighbourhood(request):
    if request.method == 'GET':
        return render(request, 'neighbourhood.html')


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def findfriend(request):
    if request.method == 'GET':
        return render(request, 'findfriend.html')
