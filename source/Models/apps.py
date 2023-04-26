import threading
from django.apps import AppConfig
from Models.utill import answerExtraction

class ModelsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Models"

    def ready(self):
        t = threading.Thread(target=answerExtraction)
        t.daemon = True
        t.start()
        