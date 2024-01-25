# myapp/urls.py
from django.urls import path
from .views import login_view, sign_up, update_user, neighbourhood, findfriend

app_name = 'backend'

urlpatterns = [
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('sign-up/', sign_up, name='signup'),
    path('update/', update_user, name='update'),
    path('neighbourhood/', neighbourhood, name='neighbourhood'),
    path('findfriend/', findfriend, name='findfriend'),
]
