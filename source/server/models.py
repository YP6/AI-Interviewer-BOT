from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Account Types
class AccountType(models.Model):
    typeTitle = models.CharField(max_length=50)
    def __str__(self):
        return self.typeTitle


# Accounts Permissions
class Permission(models.Model):
    typeID = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    permission = models.CharField(max_length=20)
    def __str__(self):
        return self.permission


# User Model
class User(AbstractUser):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    dateOfBirth = models.DateField()
    accountType = models.ForeignKey(AccountType, on_delete=models.CASCADE, null=True)
    email = models.EmailField(unique=True)
    lastModified = models.DateField(auto_now=True)
    

    def __str__(self):
        return self.username

    def register(username, password, email, firstName, lastName, gender, dateOfBirth, accountType=None):
        if(accountType):
            try:
                account = AccountType.objects.filter(typeTitle=accountType)[0]
            except:
                raise Exception("Invalid Account Type")
        else:
            account = AccountType.objects.filter(typeTitle='Interviewee')[0]

        username = User.normalize_username(username)

        if User.objects.filter(username=username).exists():
            raise Exception("Account Username Already Exists")
        
        if User.objects.filter(email=email).exists():
            raise Exception("Account Email Address Already Exists")
        
        user = User(username=username,
        email = email,
        firstName=firstName,
        lastName=lastName,
        gender=gender,
        dateOfBirth= datetime.datetime.now(),
        accountType = account)
        
        user.set_password(password)
        user.save()
        return user



class Topic(models.Model):
    topicName = models.CharField(max_length=100)
    def __str__(self):
        return self.topicName


class Interview(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    duration = models.DurationField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    def __str__(self):
        return self.title


class Question(models.Model):
    question = models.CharField(max_length=150, unique=True)
    topic = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    level = models.CharField(max_length=15)
    visibility = models.CharField(max_length=15)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.question

class QuestionAnswers(models.Model):
    questionID = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)


class InterviewQuestion(models.Model):
    questionID = models.ForeignKey(Question, on_delete=models.CASCADE)
    interviewID = models.ForeignKey(Interview, on_delete=models.CASCADE)


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
