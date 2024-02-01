import datetime
import json
import time

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .models import User, Friend

import json
from datetime import datetime

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


@csrf_exempt
@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            context = {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'location': user.location,
                    'bio': user.bio,
                    'quote': user.quote,
                    'avatar': user.avatar if user.avatar else None,
                    'blink_board': user.blink_board,
                    'blink_board_image': user.blink_board_image,
                    'updated_at': user.updated_at

                },
                'access_token': access_token,
                'refresh_token': refresh_token,
            }

            # return Response(context)

            # Render the desired template, for example 'homeProfile.html'
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
@permission_classes([IsAuthenticated])
def update_user(request):
    if request.method == 'GET':
        user = request.user
        return render(request, 'homeProfile.html', {'user': user})

    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            location = request.data.get("location", None)

            bio = request.data.get("bio", None)
            quote = request.data.get("quote", None)
            if location and len(location) > 0:
                user.location = location

            if bio and len(bio) > 0:
                user.bio = bio
            if quote and len(quote) > 0:
                user.quote = quote

            avatar_file = request.FILES.get('avatar')
            if avatar_file:
                if avatar_file.size > 0:
                    user.avatar.save(avatar_file.name, avatar_file, save=True)
                else:
                    print("Uploaded file is empty.")

            blink_board = request.data.get('blink_board', None)
            if blink_board and len(blink_board) > 0:
                user.blink_board = blink_board
                user.updated_at = datetime.datetime.now()

            avatar_file = request.FILES.get('blink_board_image')
            if avatar_file:
                if avatar_file.size > 0:
                    user.blink_board_image.save(avatar_file.name, avatar_file, save=True)
                else:
                    print("Uploaded file is empty.")
            user.save()
            return render(request, 'homeProfile.html', context={'user': user})
        else:
            print("User not authenticated!")
            return JsonResponse({'success': False, 'error': 'User not authenticated'}, status=401)


def get_neighbourhood_context(user):
    print(user.id)
    pending_request = Friend.objects.filter(user=user, status='Pending')
    accepted_request = Friend.objects.filter(user=user, status='Accepted')
    print(pending_request)
    neighbour_list = [{'username': neighbour.friend.username,
                       'avatar': neighbour.friend.avatar.url if neighbour.friend.avatar else None,
                       'blink_board': neighbour.friend.blink_board,
                       'blink_board_image': neighbour.friend.blink_board_image.url if neighbour.friend.blink_board_image else None,
                       'updated_at': neighbour.friend.updated_at, 'location': neighbour.friend.location if neighbour.friend.location else "",
                       'bio': neighbour.friend.bio if neighbour.friend.bio else "",
                       'quote': neighbour.friend.quote if neighbour.friend.quote else ""} for neighbour in
                      accepted_request]

    pending_list = [{'username': neighbour.friend.username,
                     'avatar': neighbour.friend.avatar.url if neighbour.friend.avatar else None,
                     'blink_board': neighbour.friend.blink_board,
                     'blink_board_image': neighbour.friend.blink_board_image.url if neighbour.friend.blink_board_image else None,
                     'updated_at': neighbour.friend.updated_at} for neighbour in
                    pending_request]

    context = {
        'accepted_neighbourhoods': neighbour_list,
        'pending_neighbourhoods': pending_list,
        'neighbours': json.dumps(neighbour_list,  cls=CustomJSONEncoder)
    }

    return context

@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def neighbourhood(request):
    if request.method == 'GET':
        access_token = request.GET.get('access_token')
        decoded_token = AccessToken(access_token)

        user = User.objects.filter(id=decoded_token['user_id']).first()
        context = get_neighbourhood_context(user)
        return render(request, 'neighbourhood.html', context)

    if request.method == 'POST':
        access_token = request.headers.get('Authorization', '').split('Bearer ')[-1]
        user = request.user
        username = request.data.get('username', None)
        if username:
            neighbour = Friend.objects.filter(friend__username=username, user=user).first()
            neighbour.status = 'Accepted'
            neighbour.save()
            context = get_neighbourhood_context(user)
            return redirect(reverse('backend:neighbourhood') + f'?access_token={access_token}')
        else:
            context = get_neighbourhood_context(user)
            return render(request, 'neighbourhood.html', context)


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def findfriend(request):
    if request.method == 'GET':
        return render(request, 'findfriend.html')


from django.core.serializers import serialize


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def blinkboard(request):
    if request.method == 'GET':

        access_token = request.GET.get('access_token')
        decoded_token = AccessToken(access_token)

        user = User.objects.filter(id=decoded_token['user_id']).first()

        neighbours = User.objects.filter(location__icontains=user.location).order_by('-updated_at').exclude(username=user.username)
        neighbour_list = [{'username': neighbour.username, 'avatar': neighbour.avatar.url if neighbour.avatar else None,
                           'blink_board': neighbour.blink_board, 'blink_board_image': neighbour.blink_board_image.url if neighbour.blink_board_image else None,
                           'updated_at': neighbour.updated_at} for neighbour in
                          neighbours]
        context = {
            'neighbours': neighbour_list
        }
        return render(request, 'blinkboard.html', context)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def filter_friend(request):
    if request.method == 'GET':
        user_name = request.GET.get('username')
        print(user_name)
        users = User.objects.filter(username__icontains=user_name).exclude(username=request.user.username)
        print(users)
        user_list = []

        for user in users:
            user_data = {'username': user.username}

            # Check if the avatar field has a file associated with it
            if user.avatar and user.avatar.file:
                user_data['avatar'] = user.avatar.url
            else:
                user_data['avatar'] = None  # Or any default value you prefer

            user_list.append(user_data)
        return JsonResponse({'success': True, 'users': user_list})


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    if request.method == 'POST':
        requested_username = request.data.get('username')
        user_name = request.user

        user = User.objects.get(username=requested_username)
        if not Friend.objects.filter(user=user_name, friend=user).exists():
            Friend.objects.create(user=user_name, friend=user)

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'already_friends'})
    else:
        return JsonResponse(500)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def delete_friend(request):
    if request.method == 'POST':
        access_token = request.headers.get('Authorization', '').split('Bearer ')[-1]

        requested_username = request.data.get('username')
        user_name = request.user

        user = User.objects.get(username=requested_username)
        if Friend.objects.filter(user=user_name, friend=user).exists():
            friendship = Friend.objects.filter(user=user_name, friend=user).first()
            friendship.delete()

            return redirect(reverse('backend:neighbourhood') + f'?access_token={access_token}')
        else:
            return JsonResponse({'status': 'already_friends'})
    else:
        return JsonResponse(500)