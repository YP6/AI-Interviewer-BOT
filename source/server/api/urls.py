from django.urls import path
from .views import *

urlpatterns = [
    path('help/', getAPIRoutes, name='help'),
    path('token/', OptainAuthToken, name='token'),

    path('account/login/', LoginUser, name='login'),
    path('account/logout/', LogoutUser, name='logout'),
    path('account/register/', RegisterUser, name='register'),
    path('account/profile/', CurrentProfile, name='profile'),
    path('account/edit/', EditAccount, name='edit-user'),
    path('account/attendances/', GetInterviewAttendances, name='user-attendances'),
    path('account/getAppointemnts/', GetAppointemnts, name='get-appointments'),

    path('info/accounttypes/', GetAccountTypes, name='accounttypes'),
    path('info/interviews/', GetInterviews, name='interviews'),
    path('info/interview-topics/', GetInterviewsTopics, name='interview-topics'),

    path('interview/', GetInterview, name='interview-info'),
    path('interview/add/', AddInterview, name='add-interview'),
    path('interview/edit/', EditInterview, name='edit-interview'),
    path('interview/initiate/', InitiateInterview, name='initiate-interview'),
    path('interview/getNextQuestion/', GetNextQuestion, name='get-next-question'),
    path('interview/answerQuestion', AnswerQuestion, name='answer-question'),
    path('interview/getAnswerResponse/', GetAnswerResponse, name='get-answer-response'),
    path('interview/getCreatedInterviews/', GetCreatedInterviews, name='get-created-interviews'),
    path('interview/getAttendedInterviewees/', GetAttendedInterviewees, name='get-attended-interviewees'),
        
    path('question/add/', AddQuestion, name='add-question'),
    path('question/edit/', EditQuestion, name='edit-question'),
    
    path('topic/add/', AddInterviewsTopic, name='add-topic'),

]