from pydub import AudioSegment
import os
import whisper

def toMP3(instance):
        videoPath = instance.videoPath
        
        audioPath = os.path.splitext(videoPath)[0] + '.mp3'
        
        audio = AudioSegment.from_file(videoPath)
        audio.export(audioPath, format='mp3')
        
        return str(audioPath)


def answerExtraction():
    from server.models import InterviewSession
    model = whisper.load_model("base")

    while True:           
        interviews = InterviewSession.objects.filter(processed=False)

        for interview in interviews:
            if interview.videoPath:
                audioPath = toMP3(interview) 
                result = model.transcribe(audioPath, language='en', fp16=False)
                interview.answer = result['text']
                interview.processed = True
                interview.save()