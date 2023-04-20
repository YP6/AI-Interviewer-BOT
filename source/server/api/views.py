import datetime

from moviepy.audio.AudioClip import AudioArrayClip
from pydub import AudioSegment
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .serializers import *
from ..models import yp6AuthenticationToken
from ..AUTH import CheckAuthorization, Hash, RemoveAuthorization
from .decorators import *
from django.apps import apps
from Parrot.apps import ParrotConfig
import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from moviepy.editor import VideoFileClip
from ..bot_brain.TextPreprocessing import *
import numpy as np
from moviepy.audio.io.AudioFileClip import AudioFileClip
import speech_recognition as sr
from django.views.decorators.csrf import csrf_exempt, csrf_protect


@api_view(['POST'])
@csrf_exempt
@LoggedOut
def LoginUser(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        res = Response({'OK 200' : 'Sucess', 'detail':'Authorized'}, status= status.HTTP_200_OK)
        return res
    else:
        return Response({'Error 400': 'Bad Request', 'detatil': 'Wrong Credentials'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@IsAuthenticated
def LogoutUser(request):
    respones = Response({'OK 200': 'Success', 'detail': 'Logged Out'}, status=status.HTTP_200_OK)
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
        token.userID = User.objects.get(username=request.user.username)
        dt = datetime.datetime.now()
        tokenSTR = Hash(str(request.user.id) + str(dt))
        token.token = tokenSTR
        token.signature = request.META.get('HTTP_USER_AGENT')
        token.save()
    except Exception as err:
        return Response({'Error 400': 'Bad Request', 'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)

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
        'api/interview/initiate': 'GET',
        'api/interview/getNextQuestion': 'GET',
    }
    return Response(routes)


@api_view(['POST'])
@LoggedOut
def RegisterUser(request):
    try:
        User.register(**request.data)
    except Exception as err:
        return Response({'Error 400': 'Bad Request', 'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    username = request.data['username']
    password = request.data['password']
    user = authenticate(request, username=username, password=password)
    login(request, user=user)
    return Response({'OK 200': 'Success', 'detail': 'Account Created Successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@IsAuthenticated
def GetAppointemnts(request):
    response = []
    privateInterviews = PrivateInterviewsUsers.objects.filter(userID=request.user.id)
    
    for interview in privateInterviews:
        details = Interview.objects.get(title=interview.interviewID)
        response.append(InterviewSerializer(details).data)
    
    return Response(response,status=status.HTTP_200_OK)



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
        return Response({'Error 500': 'Internal Server Error', 'detail': 'Can\'t retrieve your profile'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@IsAuthenticated
def GetInterviews(request):
    interviews = Interview.objects.all()
    serializedData = InterviewSerializer(interviews, many=True)
    for i in range(len(serializedData.data)):
        topicID = serializedData.data[i]['topic']
        topic = Topic.objects.get(id=topicID)
        serializedData.data[i]['topic'] = topic.topicName
    return Response(serializedData.data)


@api_view(['POST'])
@IsAuthenticated
def EditAccount(request):
    user = request.user
    try:
        user.edit(**request.data)
    except Exception as err:
        return Response({"Error 409": "Conflict In Database", "detail": str(err)}, status=status.HTTP_409_CONFLICT)
    return Response({"OK 200": "Account Updated Successfuly"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@IsAuthenticated
def GetInterviewAttendances(request):
    userId = request.user.id
    interviewsAttendances = InterviewAttendance.objects.filter(userID=userId)
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
    ret = []
    interviewID = request.data['id']
    interview = Interview.objects.get(id=interviewID)
    data = InterviewSerializer(interview).data
    ret.append(data)
    try:
        questionsIDs = InterviewQuestion.objects.filter(interviewID=interviewID)
    except:
        return Response({"Error 404": "No Questions Found",
                         "detail": "Interview Questions are deleted or corrupted please contact the interviewer"}
                        , status=status.HTTP_404_NOT_FOUND)
    for q in questionsIDs:
        try:
            question = Question.objects.get(question=q.questionID)
            serializedQuestion = QuestionSerializer(question, many=False)
            ret.append(serializedQuestion.data)
        except:
            return Response({"Error 404": "Some Questions are not found",
                             "detail": "Some Interview Questions are deleted please contact the interviewer"}
                            , status=status.HTTP_404_NOT_FOUND)
    return Response(ret, status=status.HTTP_200_OK)


@api_view(['POST'])
@IsAuthenticated
@CanCreateInterview
@CanCreateQuestion
def AddInterview(request):
    if 'answers' in request.data['questions'][0].keys():
        interview = Interview.add(userID=request.user, title=request.data['title'], duration=request.data['duration'],
                                topic=request.data['topic'], password=request.data['password'], isPrivate=request.data['private'])
        if interview == None:
            return Response({"Error 409": "Database Conflict", "detail": "Interview Already Exists"},
                            status=status.HTTP_409_CONFLICT)
    else:
        return Response({"Error 400": "Bad Request", "detail": "Can't Add interview without questions and answers"},
                        status=status.HTTP_400_BAD_REQUEST)

    if request.data['private']:
        for user in request.data['users']:
            if User.objects.filter(email=user).exists():
                privateInterview = PrivateInterviewsUsers.add(userID=User.objects.filter(email=user)[0], interviewID=interview)
            else:    
                return Response({"Error 400": "Bad Request", "detail": "Can't add unvalid user"},
                            status=status.HTTP_400_BAD_REQUEST)
        

    for q in request.data['questions']:
        if not 'id' in q.keys():
            try:
                if 'answers' in q.keys():
                    question = Question.add(question=q['question'], topic=q['topic'], type=q['type'],
                                            level=q['level'], visibility=q['visibility'], userID=request.user.username)
                    if not question == None:
                        InterviewQuestion.add(interview, question)
                        answer = QuestionAnswers.add(question=question, answers=q['answers'])

                    else:
                        InterviewQuestion.add(interview, Question.objects.get(question=q['question']))
            except Exception as Err:
                return Response({"Error 500": "Internal Server Error", "detail": str(Err)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                InterviewQuestion.add(interview, Question.objects.get(id=q['id']))
            except:
                return Response({"Error 404": "Question Not Found", "detail": "Can't Find Question"},
                                status=status.HTTP_404_NOT_FOUND)
    return Response({"OK 200": "Interview Added Successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@IsAuthenticated
@CanCreateInterview
@CanCreateQuestion
def EditInterview(request):
    pass


@api_view(['POST'])
@IsAuthenticated
def InitiateInterview(request):
    try:
        interview = Interview.objects.get(title=request.data['interviewID'])
        if interview.isPrivate == True:
            passwordHash = Hash(request.data['password'])
            if passwordHash != interview.password:
                return Response({"Error 403": "FORBIDDEN", "details": "Invalid Password. Try Again"}, status=status.HTTP_403_FORBIDDEN)
        
        report = Report.add(score=0, summary="")

        interviewAttendance = InterviewAttendance.add(userID=request.user.username, duration=interview.duration,
                                                      interviewID=interview, reportID=report)
        serializedData = InterviewAttendanceSerializer(interviewAttendance, many=False)

        questions = InterviewQuestion.objects.filter(interviewID=interviewAttendance.interviewID)

        for question in questions:
            interviewSession = InterviewSession.add(attendanceID=interviewAttendance, questionID=question.questionID,
                                                    answer=None)

    except Exception as Err:
        return Response({"Error 500": "Internal Server Error", "detail": str(Err)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    response = Response(status=status.HTTP_201_CREATED)
    response.set_cookie(key="attendaceID", value=interviewAttendance.id, httponly=True, secure=True)
    return Response({"attendanceID: ": interviewAttendance.id}, status=status.HTTP_200_OK)


@api_view(['POST'])
@IsAuthenticated
@CanCreateQuestion
def AddQuestion(request):
    try:
        if request.data['answers']:
            appConfig = apps.get_app_config(ParrotConfig.name)
            parrotModel = appConfig.Parrot

            question = Question.add(question=request.data['question'], topic=request.data['topic'],
                                    type=request.data['type'],
                                    level=request.data['level'], visibility=request.data['visibility'],
                                    userID=request.user.username)
            answer = QuestionAnswers.add(question=question, answers=request.data['answers'])

        # paraphrases = parrotModel.augment(input_phrase=request.data['question'])

        # for sentence in paraphrases:
        #   question = Question.add(question=sentence[0], topic=request.data['topic'],
        #                      type=request.data['type'],
        #                     level=request.data['level'], visibility=request.data['visibility'],
        #                    userID=request.user.username)
        # answer = QuestionAnswers.add(question=question, answers=request.data['answers'])

        if not question:
            return Response(
                {"Error 409": "Question Already Exist", "detail": "Can't Add Question because it's already Exist"},
                status=status.HTTP_409_CONFLICT)
    except Exception as err:
        return Response(
            {"Error 400": "Bad Request", "detail": "Can't Add Question with provided data", "more": str(err)},
            status=status.HTTP_400_BAD_REQUEST)
    return Response({"OK 200": "Success"}, status=status.HTTP_200_OK)


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
        return Response({"Error 409": "Database Conflict", "detail": "Topic Already Exists"},
                        status=status.HTTP_409_CONFLICT)
    else:
        topic = Topic(topicName=request.data['name'])
        topic.save()
    return Response({"Ok 200": "Topic Added Successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@IsAuthenticated
def GetNextQuestion(request):
    try:
        attendanceID = request.COOKIES['attendanceID']
    except Exception as err:
        return Response({"Error 400" : "Bad Request", "detail":str(err)}, status=status.HTTP_400_BAD_REQUEST)
    
    interviewQuestions = InterviewSession.objects.filter(attendanceID=attendanceID, answer=None)
    if len(interviewQuestions) == 0:
        return Response({"status": "Interview is Completed Successfully"}, status=status.HTTP_200_OK)

    question = interviewQuestions[0]
    nextQuestion = Question.objects.get(question=question.questionID)

    response = Response({"question": nextQuestion.question,
                     "topic": nextQuestion.topic}, status=status.HTTP_200_OK)
    if "questionID" in request.COOKIES:
        response.delete_cookie("questionID")
    response.set_cookie(key="questionID", value=nextQuestion.questionID, secure=True, httponly=True)
    return 


@api_view(['POST'])
@IsAuthenticated
def AnswerQuestion(request):
    try:
        attendanceId = request.COOKIES['attendanceID']
        questionId = request.COOKIES['questionID']
        videoFile = request.FILES['Video']
    except Exception as err:
        return Response({"Error 400" : "Bad Request", "detail":str(err)}, status=status.HTTP_400_BAD_REQUEST)

    videoPath = os.path.join(settings.MEDIA_ROOT, videoFile.name)
    with open(videoPath, 'wb') as f:
        for chunk in videoFile.chunks():
            f.write(chunk)
    session = InterviewSession.objects.filter(attendanceId = attendanceId, questionId=questionId)[0]
    session.videoPath = videoPath
    session.save()
    return Response({"Success": '200', 'detail':'Video Uploading Successfuly'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@IsAuthenticated
def GetAnswerResponse(request):
    attendanceId = request.data['attendanceId']
    questionId = request.data['questionId']
    session = InterviewSession.objects.filter(attendanceId = attendanceId, questionId=questionId)[0]
    if session.processed == True:
        return Response({'Accepted':'202', 'detail': session.botResponse, 'tryAgain':session.canTryAgain})
    else:
        return Response({'Waiting Model': '204 No Content', 'detail':'Try Again on a moment'}, status=status.HTTP_204_NO_CONTENT)
