from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

urlpatterns = [
    path('api/v1/users/', api_users_view, name='users'),
    path('api/v1/users/<int:user_id>/', api_user_view, name='user'),
    path('api-token-auth/', obtain_auth_token, name='login')
]