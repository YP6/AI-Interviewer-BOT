import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny


from .serializers import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .serializers import *
from ..models import yp6AuthenticationToken
from ..AUTH import CheckAuthorization,Hash,RemoveAuthorization

@api_view(['POST'])
def LoginUser(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    
        return Response({'success' : 'Authorized'})
    else:
        return Response({'Error' : 'Wrong Credentials'})
    

@login_required
@api_view(['POST'])
def LogoutUser(request):
    if not RemoveAuthorization(request):
        return Response({'Error 400': 'Bad Request'}, status=400)

    logout(request)
    
    return Response({'Success' : 'Logged Out'})



@login_required
@api_view(['GET'])
def OptainAuthToken(request):
    try:
        token = yp6AuthenticationToken()
        token.userID = User.objects.get(username = request.user.username)
        
        dt = datetime.datetime.now
        tokenSTR = Hash(str(request.user.id)+ str(dt))
        token.token = tokenSTR
        try:
            token.macAddress = request.headers['MAC']
        except:
            return Response({'Error 400 Bad Request': 'Mac Address is not provided'}, status=400)
        token.save()
    except:
        return Response({'Error 400 Bad Request': 'Unauthorized User'}, status=400)

    respones = Response(tokenSTR)
    respones.status_code = 200
    return respones




superUserTest = user_passes_test(lambda u: u.is_staff, login_url='../')

@login_required
@api_view(['GET'])
def getAPIRoutes(request):
    if not CheckAuthorization(request):
        return Response({'Error 401 Unauthorized': 'You Are Not Allowed To View This Page'}, status=401)
    routes = ['GET api/token #Optain_Auth_Token',
              'GET api/token/refresh #Refresh_Expired_Tokens', 
              'POST api/login', 
              'POST api/logout #Login_Required',
              'POST api/register',
              'GET api/info/accounttypes',
              'GET api/get-current-user-data #Login_Required', 
              'GET api/browse-interviews #Login_Required', 
              ]
    return Response(routes)


@api_view(['POST'])
def RegisterUser(request):
    
    try:
        User.register(**request.data)
    except Exception as err:
        return Response({'Error 400 Bad Request' : str(err)}, status=400)
    
    username = request.data['username']
    password = request.data['password']
    user = authenticate(request, username=username, password=password)
    login(request, user=user)
    return Response({'Account Created Successfully'}, status=200)
   

@api_view(['GET'])
def GetAccountTypes(request):
    types = AccountType.objects.all()
    serializedData = AccountTypeSerializer(types, many=True)
    return Response(serializedData.data)

