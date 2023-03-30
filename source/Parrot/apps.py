from django.apps import AppConfig
from parrot import Parrot
import torch

class ParrotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Parrot"

    def random_state(seed):
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)


    def ready(self):
        ParrotConfig.random_state(1234)
        self.Parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)