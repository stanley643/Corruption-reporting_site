from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import post_save
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

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    anonymous_name = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.anonymous_name:
            # Generate a unique anonymous name
            self.anonymous_name = generate_anonymous_name()
            while UserProfile.objects.filter(anonymous_name=self.anonymous_name).exists():
                self.anonymous_name = generate_anonymous_name()
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

# Signal to create/update UserProfile when User is created/updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    video = models.FileField(upload_to='chat_videos/', blank=True, null=True)
    document = models.FileField(upload_to='chat_documents/', blank=True, null=True)
    audio = models.FileField(upload_to='chat_audio/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}..."
    