# myapp/urls.py
from django.urls import path
from .views import login_view, sign_up, update_user, neighbourhood, findfriend, filter_friend, send_friend_request, blinkboard

app_name = 'backend'

urlpatterns = [
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('sign-up/', sign_up, name='signup'),
    path('update/', update_user, name='update'),
    path('neighbourhood/', neighbourhood, name='neighbourhood'),
    path('findfriend/', findfriend, name='findfriend'),
    path('blinkboard/', blinkboard, name='blinkboard'),
    path('filterfriend/', filter_friend, name='filterfriend'),
    path('send-request/', send_friend_request, name='send_friend_request'),
]
