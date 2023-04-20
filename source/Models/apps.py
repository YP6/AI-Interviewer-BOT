from django.apps import AppConfig
from django.apps import AppConfig
from pydub import AudioSegment
import os
import whisper


class ModelsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Models"
    
    
    def toMP3(instance):
        videoPath = instance.videoPath
        
        audioPath = os.path.splitext(videoPath)[0] + '.mp3'
        
        audio = AudioSegment.from_file(videoPath)
        audio.export(audioPath, format='mp3')
        
        return str(audioPath)


    def ready(self):
        from server.models import InterviewSession
        # model = whisper.load_model("base")
                
        interviews = InterviewSession.objects.filter(processed=False)

        # for interview in interviews:
        #     if interview.videoPath:
        #         audioPath = ModelsConfig.toMP3(interview) 
        #         result = model.transcribe(audioPath)
        #         interview.answer = result['text']
        #         interview.processed = True
        #         interview.save()