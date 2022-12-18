from django.contrib import admin
from server.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Interview)
admin.site.register(Question)
admin.site.register(Permission)
admin.site.register(AccountType)
admin.site.register(QuestionAnswers)
admin.site.register(InterviewQuestion)
admin.site.register(InterviewAttendance)
admin.site.register(Report)
admin.site.register(ReportWeakness)
admin.site.register(ReportStrengths)
