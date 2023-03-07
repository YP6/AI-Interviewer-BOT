from django.db import models
from django.contrib.auth.models import AbstractUser, Group
import datetime
from datetime import timedelta

from server.permissions import *

# Account Types
class AccountType(models.Model):
    typeTitle = models.CharField(max_length=50)
    def __str__(self):
        return self.typeTitle


# User Model
class User(AbstractUser):
    gender = models.CharField(max_length=1, null=True)
    dateOfBirth = models.DateField(null=True)
    accountType = models.ForeignKey(AccountType, on_delete=models.CASCADE, null=True)
    email = models.EmailField(unique=True)
    lastModified = models.DateField(auto_now=True)
    
    class Meta:
        permissions = [
            (CAN_CREATE_QUESTION, 'Can Create A Question'),
            (CAN_CREATE_INTERVIEW, 'Can Create an Interview'),
            (CAN_ENTER_INTERVIEW, 'Can Enter Interview'),
            (CAN_COMMENT, 'Can Type Comments'),
        ]

    def __str__(self):
        return self.username

    def register(username, password, email, first_name, last_name, gender, dateOfBirth, accountType=None):
        if gender not in ['M', 'F']:
            raise Exception("Invalid Gender")
        if(accountType):
            try:
                account = AccountType.objects.filter(typeTitle=accountType)[0]
            except:
                raise Exception("Invalid Account Type")
        else:
            account = AccountType.objects.filter(typeTitle='Interviewee')[0]
        if(len(username)<8):
            raise Exception("Username Must Be At Least 8 Characters")
        if(len(email) < 4):
            raise Exception("Incorrect Email Address")
        
        username = User.normalize_username(username)
        email = str(email).lower()
        if User.objects.filter(username=username).exists():
            raise Exception("Account Username Already Exists")
        
        if User.objects.filter(email=email).exists():
            raise Exception("Account Email Address Already Exists")

        birthDate = datetime.datetime.strptime(str(dateOfBirth), '%d-%m-%Y')
        print(birthDate)
        user = User(username=username,
        email = email,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        dateOfBirth= birthDate,
        accountType = account)
        
        
        user.set_password(password)
        user.save()
        user.groups.add(Group.objects.get(name='Default'))
        return user
    def AssignToGroup(self,groupName):
        try:
            self.groups.add(Group.objects.get(name=groupName))
        except:
            raise Exception("Invalid Group Name")
    def edit(self, username=None, password=None, email=None, first_name=None, last_name=None, accountType=None):
        if not username == None:
            if User.objects.filter(username=username).exists():
                raise Exception("Account Username Already Exists")
            else:
                username = self.normalize_username(username)
                self.username = username
        if not email == None:
            if User.objects.filter(email=email).exists():
                raise Exception("Account Email Address Already Exists")
            else:
                self.email = email
        if not password == None:
            if len(password) >= 8:
                self.set_password(password)
            else:
                raise Exception("Password Should Be 8 or more Characters")
        
        if not first_name == None:
            self.first_name = first_name
        if not last_name == None:
            self.last_name = last_name
        
        if not accountType == None:
            try:
                account = AccountType.objects.filter(typeTitle=accountType)[0]
                self.accountType = accountType
                self.groups.clear()
                self.AssignToGroup(accountType)
            except:
                raise Exception("Invalid Account Type")
        self.save()
class Topic(models.Model):
    topicName = models.CharField(max_length=100)
    def __str__(self):
        return self.topicName


class Interview(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    duration = models.IntegerField(default=2)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    def add(userID, title, duration, topic, *args, **kwargs):
        interview = Interview(userID = userID, title=title, duration = duration, topic=Topic.objects.get(topicName= topic))
        interview.save()
        return interview


class Question(models.Model):
    question = models.CharField(max_length=150, unique=True)
    topic = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    level = models.CharField(max_length=15)
    visibility = models.CharField(max_length=15)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.question
    def add(question, topic, type, level, visibility, userID):
        if Question.objects.filter(question=question).exists():
            return False
        else:
            try:
                question = Question(question=question, topic=topic, type=type, level=level, visibility=visibility, userID=User.objects.get(username=userID))
                question.save()
            except Exception as err:
                raise err
        return question
            
class QuestionAnswers(models.Model):
    questionID = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)


class InterviewQuestion(models.Model):
    questionID = models.ForeignKey(Question, on_delete=models.CASCADE)
    interviewID = models.ForeignKey(Interview, on_delete=models.CASCADE)
    def add(i, q):
        iq = InterviewQuestion(inteviewID= i, questionID=q)

# Report
class Report(models.Model):
    score = models.IntegerField()
    summary = models.CharField(max_length=255)
    

class ReportWeakness(models.Model):
    reportID = models.ForeignKey(Report, on_delete=models.CASCADE)
    weakness = models.CharField(max_length=255)
    def __str__(self):
        return self.weakness

class ReportStrengths(models.Model):
    reportID = models.ForeignKey(Report, on_delete=models.CASCADE)
    strengths = models.CharField(max_length=255)
    def __str__(self):
        return self.strengths

class InterviewAttendance(models.Model):
    reportID = models.ForeignKey(Report, on_delete=models.CASCADE)
    interviewID = models.ForeignKey(Interview, on_delete=models.CASCADE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    attendanceDate = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField()

class yp6AuthenticationToken(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    macAddress = models.TextField(null=False, default="0.0.0.0", max_length=20)
    optainedTime = models.DateTimeField(auto_now_add=True)
    token = models.TextField(null=False, default="None", max_length=64)
    expiry = models.DateTimeField(default= (datetime.datetime.now() + datetime.timedelta(days=7)))
    def __str__(self):
        return self.macAddress
