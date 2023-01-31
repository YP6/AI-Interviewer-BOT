from django.urls import path
from .views import *

urlpatterns = [
    path('help/', getAPIRoutes),
    path('token/', OptainAuthToken),
    path('login/', LoginUser),
    path('logout/', LogoutUser),
    path('register/', RegisterUser),
    path('info/accounttypes', GetAccountTypes),
    path('account/profile', CurrentProfile)
]