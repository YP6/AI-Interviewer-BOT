from rest_framework.serializers import ModelSerializer
from ..models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'date_joined', 'gender', 'dateOfBirth', 'phone', 'job', 'email', 'lastModified', 'accountType')
class OutsideUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields= ('username', 'first_name', 'last_name', 'gender', 'phone', 'job', 'email',)
class AccountTypeSerializer(ModelSerializer):
    class Meta:
        model = AccountType
        fields = ('typeTitle',)

class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class InterviewSerializer(ModelSerializer):
    class Meta:
        model = Interview
        fields = ('userID', 'title', 'duration','topic', 'isPrivate')

            
class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class ReportWeaknessSerializer(ModelSerializer):
    class Meta:
        model = ReportWeakness
        fields = '__all__'

class ReportStrengthsSerializer(ModelSerializer):
    class Meta:
        model = ReportStrengths
        fields = '__all__'

class InterviewAttendanceSerializer(ModelSerializer):
    class Meta:
        model = InterviewAttendance
        fields = ('interviewID',)

class InterviewSessionSerializer(ModelSerializer):
    class Meta:
        model = InterviewSession
        fields = ('interviewID',)
