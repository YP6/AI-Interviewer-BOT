from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('help/', getAPIRoutes),

    path('token/', getToken),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]