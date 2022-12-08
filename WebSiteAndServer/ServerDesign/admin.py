from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Report)
admin.site.register(Interview)
admin.site.register(Question)
admin.site.register(ReportWeakness)
admin.site.register(ReportStrengths)
admin.site.register(InterviewAttendance)
admin.site.register(InterviewQuestion)
admin.site.register(QuestionAnswers)


