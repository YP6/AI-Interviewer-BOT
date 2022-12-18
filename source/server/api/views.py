from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import User
from .serializers import UserSerializer
@api_view(['GET'])
def getAPIRoutes(request):
    routes = ['GET api/token','GET api/token/refresh', 'GET api/userid', 'GET api/interviews' , 'GET api/login', 'POST api/register']
    return Response(routes)

@api_view(['GET'])
def getToken(request):
    refresh = RefreshToken.for_user(UserSerializer(User.getUser('youssef', None)))
    return Response(str(refresh))

