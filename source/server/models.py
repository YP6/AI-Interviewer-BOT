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
    job = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=18, null=True)
    class Meta:
        permissions = [
            (CAN_CREATE_QUESTION, 'Can Create A Question'),
            (CAN_CREATE_INTERVIEW, 'Can Create an Interview'),
            (CAN_ENTER_INTERVIEW, 'Can Enter Interview'),
            (CAN_COMMENT, 'Can Type Comments'),
        ]

    def __str__(self):
        return self.username

    def register(username, password, email, first_name, last_name, gender, dateOfBirth, job, phone, accountType=None):
        if gender not in ['M', 'F']:
            raise Exception("Invalid Gender")
        if (accountType):
            try:
                account = AccountType.objects.filter(typeTitle=accountType)[0]
            except:
                raise Exception("Invalid Account Type")
        else:
            account = AccountType.objects.filter(typeTitle='Interviewee')[0]
        if (len(username) < 4):
            raise Exception("Username Must Be At Least 4 Characters")
        if (len(email) < 4):
            raise Exception("Incorrect Email Address")

        username = User.normalize_username(username)
        email = str(email).lower()
        if User.objects.filter(username=username).exists():
            raise Exception("Account Username Already Exists")

        if User.objects.filter(email=email).exists():
            raise Exception("Account Email Address Already Exists")

        birthDate = datetime.datetime.strptime(str(dateOfBirth), '%d-%m-%Y')
        
        user = User(username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    dateOfBirth=birthDate,
                    accountType=account,
                    job=job,
                    phone=phone)

        user.set_password(password)
        user.save()
        user.groups.add(Group.objects.get(name='Default'))
        return user

    def AssignToGroup(self, groupName):
        try:
            self.groups.add(Group.objects.get(name=groupName))
        except:
            raise Exception("Invalid Group Name")

    def edit(self, username=None, password=None, email=None, first_name=None, last_name=None, accountType=None, job=None, phone=None):
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
        
        if not self.job == None:
            self.job = job
        
        if not self.phone == None:
            self.phone = phone

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
    password = models.TextField(max_length=64,null=True)
    isPrivate = models.BooleanField(null=True)

    def __str__(self):
        return self.title

    def add(userID, title, duration, topic, password="", isPrivate=False):
        from .AUTH import Hash

        if Interview.objects.filter(title=title).exists():
            return None
        
        hash = ""
        if password:
            hash = Hash(password)

        interview = Interview(userID=userID, title=title, duration=duration, isPrivate=isPrivate, password=hash, topic=Topic.objects.get(topicName=topic))
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
            return None
        else:
            try:
                question = Question(question=question, topic=topic, type=type, level=level, visibility=visibility,
                                    userID=User.objects.get(username=userID))
                question.save()
            except Exception as err:
                raise err
        return question


class QuestionAnswers(models.Model):
    questionID = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)

    def add(question, answers):
        try:
            for answer in answers:
                questionAnswer = QuestionAnswers(questionID=Question.objects.get(question=question), answer=answer)
                questionAnswer.save()
        except Exception as err:
            raise err
        return questionAnswer


class InterviewQuestion(models.Model):
    questionID = models.ForeignKey(Question, on_delete=models.CASCADE)
    interviewID = models.ForeignKey(Interview, on_delete=models.CASCADE)

    def add(i, q):
        iq = InterviewQuestion(questionID=q, interviewID=i)
        iq.save()


# Report
class Report(models.Model):
    score = models.IntegerField()
    summary = models.CharField(max_length=255)

    def add (score, summary):
        report = Report(score=score, summary=summary)
        report.save()
        return report

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
    reportID = models.ForeignKey(Report, on_delete=models.CASCADE, null=True)
    interviewID = models.ForeignKey(Interview, on_delete=models.CASCADE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    attendanceDate = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(default=2)


    def add(userID, interviewID, duration, reportID):
        try:
            interviewAttendance = InterviewAttendance(userID=User.objects.get(username=userID), 
                                        interviewID=interviewID, duration=duration, reportID=reportID)
            interviewAttendance.save()
        except Exception as err:
            return err

        return interviewAttendance


class yp6AuthenticationToken(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    signature = models.TextField(null=False, default="0.0.0.0", max_length=20)
    optainedTime = models.DateTimeField(auto_now_add=True)
    token = models.TextField(null=False, default="None", max_length=64)
    expiry = models.DateTimeField(default=(datetime.datetime.now() + datetime.timedelta(days=7)))

    def __str__(self):
        return str(self.signature) + str(self.userID)

class InterviewResult(models.Model):
    attendanceID = models.ForeignKey(InterviewAttendance, on_delete=models.CASCADE)
    questionID = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255, null=True)
    videoPath = models.TextField(default="")
    grade = models.FloatField(default=0)
    importantWords = models.TextField(null=True)
    importantSentences = models.TextField(null=True)
    angry = models.FloatField(null=False, default=0)
    happy = models.FloatField(null=False, default=0)
    disgust = models.FloatField(null=False, default=0)
    fear = models.FloatField(null=False, default=0)
    neutral = models.FloatField(null=False, default=0)
    sad = models.FloatField(null=False, default=0)
    surprise = models.FloatField(null=False, default=0)
    status = models.CharField(max_length=6, default='Failed')
    analysed = models.BooleanField(null=False, default=False)

    def add(attendanceID, questionID, answer, videoPath, grade, importantWords, importantSentences, 
            angry=0, happy=0, disgust=0, fear=0, neutral=0, sad=0, surprise=0, analysed=False):
        try:
            interviewResult = InterviewResult(attendanceID=attendanceID, questionID=questionID, answer=answer, videoPath=videoPath,
                                            grade=grade, importantWords=importantWords, importantSentences=importantSentences, 
                                            angry = angry, happy=happy, disgust=disgust, fear=fear, neutral=neutral, sad=sad,
                                            surprise=surprise, status=("Failed" if grade < 50 else "Pass"), analysed=analysed)
            interviewResult.save()
        except Exception as err:
            return err
        return interviewResult

                                           
class InterviewSession(models.Model):
    attendanceID = models.ForeignKey(InterviewAttendance, on_delete=models.CASCADE)
    questionID = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255, null=True)
    videoPath = models.TextField(default="")
    graded = models.BooleanField(default=False)
    processed  = models.BooleanField(default=False)
    grade = models.FloatField(default=0)
    botResponse = models.TextField(default="", null=True)
    canTryAgain = models.BooleanField(default=False)
    
    def add(attendanceID, questionID, answer):
        try:
            interviewSession = InterviewSession(attendanceID=attendanceID, 
                                    questionID=questionID, answer=answer)
            interviewSession.save()

        except Exception as err:
            return err

        return interviewSession


class PrivateInterviewsUsers(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    interviewID = models.ForeignKey(Interview, on_delete=models.CASCADE)
    expiryDate = models.DateField(default=(datetime.datetime.now() + datetime.timedelta(days=7)))

    def add(userID, interviewID):
        try:
            interview = PrivateInterviewsUsers(userID=userID , interviewID=interviewID)
            interview.save()

        except Exception as err:
            return err

        return interview    