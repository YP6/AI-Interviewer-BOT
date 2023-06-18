from pydub import AudioSegment
import os
import whisper
import os


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
            try:
                if interview.videoPath and not interview.processed:
                    # Extracing answer text from the video.
                    audioPath = toMP3(interview) 
                    result = model.transcribe(audioPath, language='en', fp16=False)
                    res= result['text']
                    if res[0] == ' ':
                        res = res[1:]
                    interview.answer = res
                    interview.processed = True
                    interview.save()
                    
            except Exception as err:
                print("Speech Recognizer:",err)
                pass

