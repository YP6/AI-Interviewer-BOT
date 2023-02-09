from rest_framework.response import Response
from rest_framework import status
from ..AUTH import CheckAuthorization, RemoveAuthorization
from django.contrib.auth import logout
from ..permissions import *

# default Template for decorator
# def FunctionName(view_function):
#     def decorated_function(request, *arge, **kwargs):
#         return view_function(request, *arge, **kwargs)
#     return decorated_function

def IsAuthenticated(view_function):
    def decorated_function(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Error 400': 'Bad Request',
            "detail" : "Login Required."},
            status=status.HTTP_400_BAD_REQUEST)

        elif not 'Authorization' in request.headers:
            return Response({'Error 400': 'Bad Request',
            "detail": "Authorization required."}, 
            status=status.HTTP_400_BAD_REQUEST)

        elif not 'MAC' in request.headers:
            return Response({'Error 400': 'Bad Request',
            "detail": "MAC required."}, 
            status=status.HTTP_400_BAD_REQUEST)

        elif not CheckAuthorization(request):
            #logout(request)
            return Response({'Error 401':'Unauthorized User',
            'detail': 'Invalid or Expired Auth Token Please Login Again'}, 
            status= status.HTTP_401_UNAUTHORIZED)

        return view_function(request, *args, **kwargs)
    return decorated_function

def LoggedOut(view_function):
    def decorated_function(request, *arge, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            try:
                RemoveAuthorization(request)
            except:
                pass
            return Response({'Error 400': 'Bad Request',
            "detail": "You must log Out in order to register a new account"}, 
            status=status.HTTP_400_BAD_REQUEST)
        return view_function(request, *arge, **kwargs)
    return decorated_function
    
def CanCreateQuestion(view_function):
    def decorated_function(request, *args, **kwargs):
        if request.user.has_perm('server.'+CAN_CREATE_QUESTION):
            return view_function(request, *args, **kwargs)
        else:
            return Response({'Error 401':'Unauthorized User',
            'detail': "You Don't Have Permession to perform this action."}, 
            status= status.HTTP_401_UNAUTHORIZED)
    return decorated_function

def CanCreateInterview(view_function):
    def decorated_function(request, *args, **kwargs):
        if request.user.has_perm('server.'+CAN_CREATE_INTERVIEW):
            return view_function(request, *args, **kwargs)
        else:
            return Response({'Error 401':'Unauthorized User',
            'detail': "You Don't Have Permession to perform this action."}, 
            status= status.HTTP_401_UNAUTHORIZED)
    return decorated_function

def CanComment(view_function):
    def decorated_function(request, *args, **kwargs):
        if request.user.has_perm('server.'+CAN_COMMENT):
            return view_function(request, *args, **kwargs)
        else:
            return Response({'Error 401':'Unauthorized User',
            'detail': "You Don't Have Permession to perform this action."}, 
            status= status.HTTP_401_UNAUTHORIZED)
    return decorated_function