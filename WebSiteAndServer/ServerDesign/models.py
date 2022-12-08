from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Report(models.Model):
    Score = models.IntegerField(max_length=10)
    Summary = models.CharField(max_length=255)


class Interview(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)


class Question(models.Model):
    TheQuestion = models.CharField(max_length=150, unique=True)
    Topic = models.CharField(max_length=50)
    Type = models.CharField(max_length=50)
    Level = models.CharField(max_length=15)
    Visibility = models.CharField(max_length=15)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)


class ReportWeakness(models.Model):
    ReportID = models.ForeignKey(Report, on_delete=models.CASCADE)
    Weakness = models.CharField(max_length=255)


class ReportStrengths(models.Model):
    ReportID = models.ForeignKey(Report, on_delete=models.CASCADE)
    Strengths = models.CharField(max_length=255)


class InterviewAttendance(models.Model):
    ReportID = models.ForeignKey(Report, on_delete=models.CASCADE)
    InterviewID = models.ForeignKey(Interview, on_delete=models.CASCADE, db_column='InterviewID')
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, db_column='UserID')
    AttendanceData = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False  # for CompositePK *1
        db_table = 'InterviewAttendance'
        unique_together = (('ReportID', 'InterviewID', 'UserID'),)


class InterviewQuestion(models.Model):
    QuestionID = models.ForeignKey(Question, on_delete=models.CASCADE, db_column='QuestionID')
    InterviewID = models.ForeignKey(Interview, on_delete=models.CASCADE, db_column='InterviewID')

    class Meta:
        managed = False  # for CompositePK *1
        db_table = 'InterviewQuestion'
        unique_together = (('QuestionID', 'InterviewID'),)


class QuestionAnswers(models.Model):
    QuestionID = models.ForeignKey(Question, on_delete=models.CASCADE)
    Answer = models.CharField(max_length=255)
