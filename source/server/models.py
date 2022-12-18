from django.db import models
from django.contrib.auth.models import AbstractUser


# Account Types
class AccountType(models.Model):
    typeTitle = models.CharField(max_length=50)


# Accounts Permissions
class Permission(models.Model):
    typeID = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    permission = models.CharField(max_length=20)


# User Model
class User(AbstractUser):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    dateOfBirth = models.DateField(auto_now=True)
    accountType = models.ForeignKey(AccountType, on_delete=models.CASCADE, null=True)
    email = models.EmailField(unique=True)


class Topic(models.Model):
    topicName = models.CharField(max_length=100)


class Interview(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    duration = models.DurationField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)


class Question(models.Model):
    question = models.CharField(max_length=150, unique=True)
    topic = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    level = models.CharField(max_length=15)
    visibility = models.CharField(max_length=15)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)


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


class ReportStrengths(models.Model):
    reportID = models.ForeignKey(Report, on_delete=models.CASCADE)
    strengths = models.CharField(max_length=255)


class InterviewAttendance(models.Model):
    reportID = models.ForeignKey(Report, on_delete=models.CASCADE)
    interviewID = models.ForeignKey(Interview, on_delete=models.CASCADE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    attendanceDate = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField()


class InterviewQuestion(models.Model):
    questionID = models.ForeignKey(Question, on_delete=models.CASCADE, db_column='QuestionID')
    interviewID = models.ForeignKey(Interview, on_delete=models.CASCADE, db_column='InterviewID')