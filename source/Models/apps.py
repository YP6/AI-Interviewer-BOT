import threading
from django.apps import AppConfig
from .SpeechRecognizer import answerExtraction
from .QuestionGrader import QuestionGrader
from .EmotionRecognizer import EmotionRecognizer

class ModelsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Models"

    def ready(self):
        speechRecpgnition = threading.Thread(target=answerExtraction)
        speechRecpgnition.daemon = True
        speechRecpgnition.start()

        nlpModel = threading.Thread(target=QuestionGrader)
        nlpModel.daemon = True
        nlpModel.start()

        cvModel = threading.Thread(target=EmotionRecognizer)
        cvModel.daemon = True
        cvModel.start()