import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .serializers import *
from ..models import yp6AuthenticationToken
from ..AUTH import CheckAuthorization,Hash,RemoveAuthorization
from .decorators import *




@api_view(['POST'])
@LoggedOut
def LoginUser(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    
        return Response({'OK 200' : 'Sucess', 'detatil':'Authorized'}, status= status.HTTP_200_OK)
    else:
        return Response({'Error 400' : 'Bad Request','detatil':'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@IsAuthenticated
def LogoutUser(request):
    respones = Response({'OK 200':'Success', 'detail':'Logged Out'}, status=status.HTTP_200_OK)
    respones.delete_cookie('csrftoken')
    if not RemoveAuthorization(request):
        return Response({'Error 400': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
    logout(request)
    
    return respones



@api_view(['GET'])
@login_required
def OptainAuthToken(request):
    try:
        token = yp6AuthenticationToken()
        token.userID = User.objects.get(username = request.user.username)
        dt = datetime.datetime.now()
        tokenSTR = Hash(str(request.user.id)+ str(dt))
        token.token = tokenSTR
        try:
            token.macAddress = request.headers['MAC']
        except:
            return Response({'Error 400': 'Bad Request', 'detatil': 'Mac Address is not Provided'}, status=status.HTTP_400_BAD_REQUEST)
        token.save()
    except:
        return Response({'Error 400': 'Bad Request', 'detail':'Unauthorized User'}, status=status.HTTP_400_BAD_REQUEST)

    respones = Response(tokenSTR)
    respones.status_code = 200
    return respones




superUserTest = user_passes_test(lambda u: u.is_staff, login_url='../')

@api_view(['GET'])
def getAPIRoutes(request):
    routes = {
        'api/token': 'GET',
        'api/account/login': 'POST', 
        'api/account/logout': 'POST',
        'api/account/register': 'POST',
        'api/account/profile': 'GET',
        'api/account/edit/': 'POST',
        'api/account/attendances/': 'GET',
        'api/info/accounttypes': 'GET',
        'api/info/interviews': 'GET',
        'api/info/interview-topics/': 'GET',
        'api/interview/': 'GET',
        'api/interview/add/': 'POST',
        'api/interview/edit/': 'POST',
        'api/question/add/': 'POST',
        'api/question/edit/': 'POST',
        'api/topic/add/': 'POST',
    }
    return Response(routes)


@api_view(['POST'])
@LoggedOut
def RegisterUser(request):
    try:
        User.register(**request.data)
    except Exception as err:
        return Response({'Error 400': 'Bad Request' , 'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)
    
    username = request.data['username']
    password = request.data['password']
    user = authenticate(request, username=username, password=password)
    login(request, user=user)
    return Response({'OK 200':'Success','detail':'Account Created Successfully'}, status=status.HTTP_200_OK)
   

@api_view(['GET'])
def GetAccountTypes(request):
    types = AccountType.objects.all()
    serializedData = AccountTypeSerializer(types, many=True)
    return Response(serializedData.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@IsAuthenticated
def CurrentProfile(request):
    user = UserSerializer(request.user, many=False)
    if user.is_valid:
        return Response(user.data)
    else:
        return Response({'Error 500' :  'Internal Server Error','detail': 'Can\'t retrieve your profile'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@IsAuthenticated
def GetInterviews(request):
    interviews = Interview.objects.all()
    serializedData = InterviewSerializer(interviews, many=True)
    return Response(serializedData.data)

@api_view(['POST'])
@IsAuthenticated
def EditAccount(request):
    user = request.user
    try:
        user.edit(**request.data)
    except Exception as err:
        return Response({"Error 409":"Conflict In Database", "detail" : str(err)}, status=status.HTTP_409_CONFLICT)
    return Response({"OK 200":"Account Updated Successfuly"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@IsAuthenticated
def GetInterviewAttendances(request):
    userId = request.user.id
    interviewsAttendances = InterviewAttendance.objects.filter(userID = userId)
    serializedData = InterviewAttendanceSerializer(interviewsAttendances, many=True)
    return Response(serializedData.data)

@api_view(['GET'])
@IsAuthenticated
def GetInterviewsTopics(request):
    topics = Topic.objects.all()
    serializedData = TopicSerializer(topics, many=True)
    return Response(serializedData.data)

@api_view(['GET'])
@IsAuthenticated
def GetInterview(request):
    ret=[]
    interviewID = request.data['id']
    interview = Interview.objects.get(id=interviewID)
    data = InterviewSerializer(interview).data
    ret.append(data)
    try:
        questionsIDs = InterviewQuestion.objects.filter(interviewID=interviewID)
    except:
        return Response({"Error 404":"No Questions Found", 
        "detail":"Interview Questions are deleted or corrupted please contact the interviewer"}
        , status=status.HTTP_404_NOT_FOUND)
    for q in questionsIDs:
        try:
            question = Question.objects.get(question=q.questionID)
            serializedQuestion = QuestionSerializer(question, many=False)
            ret.append(serializedQuestion.data)
        except:
            return Response({"Error 404":"Some Questions are not found", 
            "detail":"Some Interview Questions are deleted please contact the interviewer"}
            , status=status.HTTP_404_NOT_FOUND)
    return Response(ret, status=status.HTTP_200_OK)

@api_view(['POST'])
@IsAuthenticated
@CanCreateInterview
@CanCreateQuestion
def AddInterview(request):
    interview = Interview.add(request.user, **request.data)
    for q in request.data['questions']:
        if not 'id' in q.keys():
            try:
                question = Question.add(question=q['question'], topic=q['topic'], type=q['type'],
                    level=q['level'], visibility=q['visibility'], userID=request.user.username)
                if not question == None:
                    InterviewQuestion.add(interview, question)
                else:
                    InterviewQuestion.add(interview, Question.objects.get(question=q['question']))
            except Exception as Err:
                return Response({"Error 500" : "Internal Server Error", "detail":str(Err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                InterviewQuestion.add(interview, Question.objects.get(id=q['id']))
            except:
                return Response({"Error 404" : "Question Not Found", "detail":"Can't Find Question"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"OK 200":"Interview Added Successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@IsAuthenticated
@CanCreateInterview
@CanCreateQuestion
def EditInterview(request):
    pass

@api_view(['POST'])
@IsAuthenticated
@CanCreateQuestion
def AddQuestion(request):
    try:
        question = Question.add(question=request.data['question'], topic=request.data['topic'], type=request.data['type'],
            level=request.data['level'], visibility=request.data['visibility'], userID=request.user.username)
        if not question:
            return Response({"Error 409" : "Question Already Exist", "detail":"Can't Add Question because it's already Exist"}, status=status.HTTP_409_CONFLICT)
    except Exception as err:
        return Response({"Error 400" : "Bad Request", "detail":"Can't Add Question with provided data", "more":str(err)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"OK 200":"Success"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@IsAuthenticated
@CanCreateQuestion
def EditQuestion(request):
    pass


@api_view(['POST'])
@IsAuthenticated
@CanCreateInterview
def AddInterviewsTopic(request):
    if Topic.objects.filter(topicName=request.data['name']).exists():
        return Response({"Error 409":"Database Conflict", "detail" :"Topic Already Exists"}, status=status.HTTP_409_CONFLICT)
    else:
        topic = Topic(topicName=request.data['name'])
        topic.save()
    return Response({"Ok 200":"Topic Added Successfully"}, status=status.HTTP_200_OK)