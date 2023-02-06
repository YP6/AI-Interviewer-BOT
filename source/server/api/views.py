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
    
        return Response({'success' : 'Authorized'})
    else:
        return Response({'Error' : 'Wrong Credentials'})
    

@api_view(['POST'])
@IsAuthenticated
def LogoutUser(request):
    if not RemoveAuthorization(request):
        return Response({'Error 400': 'Bad Request'}, status=400)

    logout(request)
    
    return Response({'Success' : 'Logged Out'})



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
            return Response({'Error 400 Bad Request': 'Mac Address is not provided'}, status=400)
        token.save()
    except:
        return Response({'Error 400 Bad Request': 'Unauthorized User'}, status=400)

    respones = Response(tokenSTR)
    respones.status_code = 200
    return respones




superUserTest = user_passes_test(lambda u: u.is_staff, login_url='../')

@api_view(['GET'])
def getAPIRoutes(request):
    routes = {
        'api/token': 'GET',
        'api/login': 'POST', 
        'api/logout': 'POST',
        'api/register': 'POST',
        'api/info/accounttypes': 'GET',
        'api/account/profile': 'GET',
        'api/info/interviews': 'GET',
        'api/account/edit/': 'POST',
        'account/attendances/': 'GET',
        'info/interview-topics/': 'GET',
        'interview/': 'GET',
        'interview/add/': 'POST',
        'interview/edit/': 'POST',
        'question/add/': 'POST',
        'question/edit/': 'POST',
        'topic/add/': 'POST',
    }
    return Response(routes)


@api_view(['POST'])
@LoggedOut
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


@api_view(['GET'])
@IsAuthenticated
def CurrentProfile(request):
    user = UserSerializer(request.user, many=False)
    if user.is_valid:
        return Response(user.data)
    else:
        return Response({'500 Internal Server Error': 'Can\'t retrieve your profile'}, status=500)


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
    interview = Interview.add(**request.data)
    for q in request.data['questions']:
        if q['id'] == None:
            try:
                question = Question.add(question=q['question'], topic=q['topic'], type=q['type'],
                    level=q['level'], visibility=q['visibility'], userID=request.user.username)
                if question:
                    InterviewQuestion.add(interview, question)
                else:
                    InterviewQuestion.add(interview, Question.objects.get(question=q['question']))
            except:
                return Response({"Error 500" : "Internal Server Error", "detail":"Can't Add Question"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
    if Topic.objects.filter(topicName=request.data['name']).exists:
        return Response({"Error 400":"Bad Request", "detail" :"Topic Already Exists"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        topic = Topic(topicName=request.data['name'])
        topic.save()
    return Response({"Ok 200":"Topic Added Successfully"}, status=status.HTTP_200_OK)