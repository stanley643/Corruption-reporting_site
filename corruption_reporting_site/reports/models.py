from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
import random
class Report(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    evidence_file = models.FileField(upload_to='evidences/')

# Helper function to generate a random anonymous name
def generate_anonymous_name():
    adjectives = ["Clever", "Anonymous", "Invisible", "Mysterious", "Silent", "Hidden"]
    nouns = ["Reporter", "Whistleblower", "Informant", "Messenger", "Witness"]
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    number = random.randint(0, 999)
    return f"{adjective}{noun}{number}"
